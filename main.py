import asyncio
import json
import os
import sys
from dotenv import load_dotenv

from filter_pr_helper import filter_patch
from src.github_tools.github_comment import send_github_comment
from src.agent.pr_bot_agent import PRBotAgent
from src.utility.fetch_utility import fetch_github_file, fetch_github_patch
from src.utility.model_loader import ClassicILLMLoader


async def main():
    load_dotenv()

    sha = os.getenv('SHA')
    token = os.getenv('BOT_GH_TOKEN')

    if len(sys.argv) < 2:
        print("Usage: python my_script.py <patch_file>")
        sys.exit(1)

    github_event_raw_json = sys.argv[1]
    github_event_json = json.loads(github_event_raw_json)
    patch_content = await fetch_github_patch(pull_request_url=github_event_json['pull_request']['url'], token=token)

    print(patch_content)

    # try:
    #     with open(patch_file, 'r') as file:
    #         patch_lines = file.readlines()
    #
    #         filtered_p = ''.join(filter_patch(patch_lines))
    #
    #         # Get the custom instruction
    #         c_instruction = fetch_github_file(content_url=content_url, file_path='pull_request_bot_instruction.txt',
    #                           sha=sha, token=token)
    #
    #         agent = PRBotAgent(ClassicILLMLoader())
    #         agent_graph = agent.create_graph()
    #
    #         feedback_content = agent_graph.invoke({
    #             'pr_patch': filtered_p,
    #             'custom_instruction': c_instruction,
    #         },
    #         {'run_name': 'PR Agent'})
    #
    #         send_github_comment(comment_url, feedback_content['plan'])
    #
    # except Exception as e:
    #     print(f"Error reading {patch_file}: {e}")
    #     sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
