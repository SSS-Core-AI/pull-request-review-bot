import asyncio
import json
import os
import sys
import uuid

from dotenv import load_dotenv

from src.agent.file_crawler.file_crawler_tool import FileCrawlerTool
from src.agent.pull_request.pr_agent_tool import get_comment_content
from src.github_tools.github_comment import send_github_comment, fetch_github_content
from src.model.pull_request_model import PullRequestIssueModel
from src.repo.pr_agent_repo import PRAgentRepo
from src.utility.fetch_utility import fetch_github_file, fetch_github_patch, fetch_github_files
from src.utility.llm_state import LLMAPIConfig
from src.utility.static_variable import CUSTOM_INSTRUCTION_FILE

async def process_review(session_id: str, token: str, sha: str, comment_url: str,
                         content_url: str, self_repo_url: str, pull_request_url: str):
    api_config = LLMAPIConfig.get_config()
    pr_repo = PRAgentRepo(session_id, api_config)

    file_repo_url = self_repo_url+'/files'

    async with asyncio.TaskGroup() as tg:
        patch_content_task = tg.create_task(
            fetch_github_patch(pull_request_url=pull_request_url, token=token)
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

    await send_github_comment(comment_url, summary, token)

    # Issue comment agent
    feedback_contents: list[PullRequestIssueModel] = await pr_repo.run_pr_agent(patch_content=patch_content,
                                                   c_instruction=c_instruction,
                                                   file_crawler=file_crawler,
                                                   short_summary=summary)

    async with asyncio.TaskGroup() as tg:
        for feedback_content in feedback_contents:
            pull_comment_url = comment_url.replace('/issues/', '/pulls/')

            tg.create_task(
                send_github_comment(pull_comment_url, get_comment_content(feedback_content), token,
                                    sha=sha, file_path=feedback_content.file_path, line_number=feedback_content.line_number)
            )

async def process_comment(session_id: str, token: str, github_event_json: dict):
    if  'pull_request' not in github_event_json['issue']:
        return

    comment_url = github_event_json['issue']['comments_url']
    repo_url = github_event_json['issue']['pull_request']['url']

    page_comment_contents = await fetch_github_content(comment_url+"?per_page=10", token)
    print('page_comment_contents', page_comment_contents['link_header'])

    comment_contents = (await fetch_github_content(comment_url, token))['data']
    repo_contents = (await fetch_github_content(repo_url, token))['data']
    last_comment = comment_contents[-1]['body']

    if last_comment == '/comment':
        await process_review(session_id=session_id, token=token,
                             sha=repo_contents['head']['sha'],
                             comment_url=repo_contents['comments_url'],
                             content_url=repo_contents['head']['repo']['contents_url'],
                             self_repo_url=repo_contents['_links']['self']['href'],
                             pull_request_url=repo_contents['url'])

async def main(github_event_json: dict):
    load_dotenv()
    session_id = str(uuid.uuid4())
    token = os.getenv('BOT_GH_TOKEN')

    event_name = os.getenv('EVENT_NAME')

    if event_name == 'issue_comment':
        await process_comment(session_id, token, github_event_json)
    else:
        sha = github_event_json['pull_request']['head']['sha']
        comment_url = github_event_json['pull_request']['comments_url']
        content_url = github_event_json['repository']['contents_url']
        self_repo_url = github_event_json['pull_request']['_links']['self']['href']
        pull_request_url = github_event_json['pull_request']['url']
        await process_review(session_id=session_id, token=token, sha=sha, comment_url=comment_url,
                             content_url=content_url, self_repo_url=self_repo_url, pull_request_url=pull_request_url)

if __name__ == "__main__":
    asyncio.run(main( json.loads(sys.argv[1]) ))
