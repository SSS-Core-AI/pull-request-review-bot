from src.agent.pull_request.pr_bot_agent import PRBotAgent
from src.github_tools.github_files import fetch_full_files, find_import_scripts_str
from src.model.pull_request_model import FileModel
from src.utility.llm_state import LLMAPIConfig
from src.utility.model_loader import ClassicILLMLoader


class PRAgentRepo:
    def __init__(self, api_config: LLMAPIConfig, content_url: str, sha: str, token: str):
        self._api_config = api_config
        self._content_url = content_url
        self._sha = sha
        self._token = token

    async def preprocessing(self, commit_file_array: list[FileModel]):
        commit_file_array, full_concat_script = await fetch_full_files(commit_file_array, self._content_url, self._sha, self._token)
        dependency_full_str = find_import_scripts_str(commit_file_array)

        print('dependency_full_str', dependency_full_str)

    def run_agent(self, patch_content: str, c_instruction: str):
        agent = PRBotAgent(ClassicILLMLoader(self._api_config))
        agent_graph = agent.create_graph()

        feedback_content = agent_graph.invoke({
            'pr_patch': patch_content,
            'custom_instruction': c_instruction,
        },
        {'run_name': 'PR Agent'})

        return feedback_content['plan']