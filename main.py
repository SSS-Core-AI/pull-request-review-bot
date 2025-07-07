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
from src.utility.static_variable import CUSTOM_INSTRUCTION_FILE

async def main(github_event_json: dict):
    load_dotenv()
    session_id = str(uuid.uuid4())

    api_config = LLMAPIConfig.get_config()
    token = os.getenv('BOT_GH_TOKEN')

    pr_repo = PRAgentRepo(session_id, api_config)

    sha = github_event_json['pull_request']['head']['sha']
    comment_url = github_event_json['pull_request']['comments_url']
    content_url = github_event_json['repository']['contents_url']
    self_repo_url = github_event_json['pull_request']['_links']['self']['href']
    file_repo_url = self_repo_url+'/files'

    async with asyncio.TaskGroup() as tg:
        patch_content_task = tg.create_task(
            fetch_github_patch(pull_request_url=github_event_json['pull_request']['url'], token=token)
        )

        # Get the custom instruction
        c_instruction_task = tg.create_task(
            fetch_github_file(content_url=content_url, file_path=CUSTOM_INSTRUCTION_FILE,
                              sha=sha, token=token)
        )

        # Fetch a commit file list
        commit_files_task = tg.create_task(
            fetch_github_files(file_repo_url, token=token)
        )

    patch_content = patch_content_task.result()
    c_instruction = c_instruction_task.result()
    commit_file_array = commit_files_task.result()

    file_crawler = FileCrawlerTool(commit_file_array, content_url=content_url, sha=sha, token=token)
    summary = await pr_repo.run_summary_agent(patch_content=patch_content)


    await send_github_comment(comment_url, summary)

    # Issue comment agent
    feedback_contents = await pr_repo.run_pr_agent(patch_content=patch_content, c_instruction=c_instruction, file_crawler=file_crawler)

    async with asyncio.TaskGroup() as tg:
        for feedback_content in feedback_contents:
            tg.create_task(
                send_github_comment(comment_url, feedback_content)
            )


if __name__ == "__main__":
    asyncio.run(main( json.loads(sys.argv[1]) ))
