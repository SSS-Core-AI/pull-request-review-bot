import asyncio
import json
import os
import sys
import uuid

from dotenv import load_dotenv

from src.agent.file_crawler.file_crawler_tool import FileCrawlerTool
from src.github_tools.github_comment import send_github_comment
from src.repo.pr_agent_repo import PRAgentRepo
from src.utility.fetch_utility import fetch_github_file, fetch_github_patch, fetch_github_files
from src.utility.llm_state import LLMAPIConfig


async def main(github_event_json: dict):
    load_dotenv()
    session_id = uuid.uuid4()

    api_config = LLMAPIConfig.get_config()
    token = os.getenv('BOT_GH_TOKEN')

    patch_content = await fetch_github_patch(pull_request_url=github_event_json['pull_request']['url'], token=token)

    sha = github_event_json['pull_request']['head']['sha']
    comment_url = github_event_json['pull_request']['comments_url']
    content_url = github_event_json['repository']['contents_url']
    self_repo_url = github_event_json['pull_request']['_links']['self']['href']
    file_repo_url = self_repo_url+'/files'

    # Get the custom instruction
    c_instruction = await fetch_github_file(content_url=content_url, file_path='pull_request_bot_instruction.txt',
                      sha=sha, token=token)

    commit_file_array = await fetch_github_files(file_repo_url, token=token)

    file_crawler = FileCrawlerTool(commit_file_array, content_url=content_url, sha=sha, token=token)

    pr_repo = PRAgentRepo(api_config, file_crawler)
    feedback_contents = await pr_repo.run_pr_agent(patch_content=patch_content, c_instruction=c_instruction)
    send_github_comment(comment_url, '\n\n'.join(feedback_contents))


if __name__ == "__main__":
    asyncio.run(main( json.loads(sys.argv[1]) ))
