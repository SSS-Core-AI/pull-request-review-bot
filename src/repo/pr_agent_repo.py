import asyncio

from src.agent.pr_bot_agent import PRBotAgent
from src.model.pull_request_model import FileModel
from src.utility.fetch_utility import fetch_github_file
from src.utility.llm_state import LLMAPIConfig
from src.utility.model_loader import ClassicILLMLoader


class PRAgentRepo:
    def __init__(self, api_config: LLMAPIConfig, content_url: str, sha: str, token: str):
        self._api_config = api_config
        self._content_url = content_url
        self._sha = sha
        self._token = token

    async def preprocessing(self, commit_file_array: list[FileModel]):
        tasks = []
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(fetch_github_file(self._content_url, file.filename, self._sha, self._token))
                for file in commit_file_array
            ]

        results = [task.result() for task in tasks]
        print("Results:", results)

    def run_agent(self, patch_content: str, c_instruction: str):
        agent = PRBotAgent(ClassicILLMLoader(self._api_config))
        agent_graph = agent.create_graph()

        feedback_content = agent_graph.invoke({
            'pr_patch': patch_content,
            'custom_instruction': c_instruction,
        },
        {'run_name': 'PR Agent'})

        return feedback_content['plan']