import asyncio
import json
import os
import sys
from dotenv import load_dotenv

from src.github_tools.github_comment import send_github_comment
from src.agent.pull_request.pr_bot_agent import PRBotAgent
from src.repo.pr_agent_repo import PRAgentRepo
from src.utility.fetch_utility import fetch_github_file, fetch_github_patch, fetch_github_files
from src.utility.llm_state import LLMAPIConfig
from src.utility.model_loader import ClassicILLMLoader


async def main():
    load_dotenv()

    api_config = LLMAPIConfig.get_config()
    token = os.getenv('BOT_GH_TOKEN')

    github_event_raw_json = sys.argv[1]
    github_event_json = json.loads(github_event_raw_json)
    patch_content = await fetch_github_patch(pull_request_url=github_event_json['pull_request']['url'], token=token)

    sha = github_event_json['pull_request']['head']['sha']
    comment_url = github_event_json['pull_request']['comments_url']
    content_url = github_event_json['repository']['contents_url']
    self_repo_url = github_event_json['pull_request']['_links']['self']['href']
    file_repo_url = self_repo_url+'/files'

    try:
        # Get the custom instruction
        c_instruction = await fetch_github_file(content_url=content_url, file_path='pull_request_bot_instruction.txt',
                          sha=sha, token=token)

        commit_file_array = await fetch_github_files(file_repo_url, token=token)

        pr_repo = PRAgentRepo(api_config, content_url, sha, token)
        await pr_repo.preprocessing(commit_file_array)

        pr_repo.run_agent(patch_content=patch_content, c_instruction=c_instruction)
        agent = PRBotAgent(ClassicILLMLoader(api_config))
        agent_graph = agent.create_graph()

        feedback_content = agent_graph.invoke({
            'pr_patch': patch_content,
            'custom_instruction': c_instruction,
        },
        {'run_name': 'PR Agent'})

        send_github_comment(comment_url, feedback_content['plan'])

    except Exception as e:
        print(f"Error reading {patch_content}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
