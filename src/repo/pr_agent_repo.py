import os

from src.agent.file_crawler.file_crawler_tool import FileCrawlerTool
from src.agent.pull_request.pr_bot_agent import PRBotAgent
from src.utility.llm_state import LLMAPIConfig
from src.utility.model_loader import ClassicILLMLoader
from langfuse.langchain import CallbackHandler

langfuse_handler = CallbackHandler()

class PRAgentRepo:
    def __init__(self, api_config: LLMAPIConfig, file_crawler: FileCrawlerTool):
        self._api_config = api_config
        self._file_crawler = file_crawler
        self._langfuse_handler = CallbackHandler(public_key=os.getenv('LANGFUSE_PUBLIC_KEY'))

    async def run_pr_agent(self, patch_content: str, c_instruction: str):
        agent = PRBotAgent(ClassicILLMLoader(self._api_config), self._file_crawler)
        agent_graph = agent.create_graph()

        feedback_content = await agent_graph.ainvoke({
            'pr_patch': patch_content,
            'custom_instruction': c_instruction,
        },
        {'run_name': 'PR bot Agent', "callbacks": [self._langfuse_handler] })

        return feedback_content['plan']