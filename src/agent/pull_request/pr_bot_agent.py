from langchain_core.output_parsers import StrOutputParser
from langgraph.constants import END
from langgraph.graph import StateGraph

from src.agent.file_crawler.file_crawler_prompt import FILE_CRAWLER_SYSTEM_PROMPT, FILE_CRAWLER_HUMAN_PROMPT
from src.agent.file_crawler.file_crawler_tool import FileCrawlerTool
from src.agent.pull_request.pr_agent_tool import get_custom_instruction
from src.agent.pull_request.pr_bot_state import ChatbotAgentState
from src.agent.pull_request.pr_draft_prompt import PR_DRAFT_SYSTEM_PROMPT, PR_DRAFT_HUMAN_PROMPT
from src.agent.pull_request.pr_plan_prompt import PLAN_SYSTEM_PROMPT, PLAN_HUMAN_PROMPT
from src.utility.model_loader import ILLMLoader
from src.utility.module_prompt_factory import ModulePromptFactory
from src.utility.utility_func import parse_json


class PRBotAgent:
    def __init__(self, llm_loader: ILLMLoader, file_crawler: FileCrawlerTool):
        self._llm_loader = llm_loader
        self._file_crawler = file_crawler

    async def _file_preparation(self, state: ChatbotAgentState):
        """ Get all the file dependencies path """
        commit_file_array, commit_file_concat_str, file_dependencies_str = await self._file_crawler.search_script_contents(self._file_crawler.commit_file_array)
        self._file_crawler.commit_file_array = commit_file_array

        return {'file_commit_concat_text': commit_file_concat_str,'file_dependency_paths_text': file_dependencies_str}

    async def _llm_file_dependency_path(self, state: ChatbotAgentState):
        """ Grab and fetch the script content from all dependencies """
        llm = self._llm_loader.get_llm_model()
        simple_chain = ModulePromptFactory(
            StrOutputParser(),
            model=llm,
            name='File crawler',
            system_prompt_text=FILE_CRAWLER_SYSTEM_PROMPT,
            human_prompt_text=FILE_CRAWLER_HUMAN_PROMPT,
        ).create_chain()

        r = await (simple_chain.with_config({"run_name": "File crawler"}).ainvoke({'file_dependency_paths_text': state['file_dependency_paths_text']}))
        dependencies_list: list[dict] = parse_json(r)

        await self._file_crawler.fetch_llm_files_content(dependencies_list)

        return {'file_lookup_table': self._file_crawler.file_table}

    async def _llm_pr_draft_plan(self, state: ChatbotAgentState):
        llm = self._llm_loader.get_llm_model()
        simple_chain = ModulePromptFactory(
            StrOutputParser(),
            model=llm,
            name='PR Brief',
            system_prompt_text=PR_DRAFT_SYSTEM_PROMPT,
            human_prompt_text=PR_DRAFT_HUMAN_PROMPT,
        ).create_chain()

        r = await (simple_chain.with_config({"run_name": "PR Brief"}).ainvoke({
            'pr_patch': state['pr_patch'],
            'custom_instruction': get_custom_instruction(state['custom_instruction']),
            'committed_file_and_dependency': self._file_crawler.get_commit_files_dependencies_str(),
        }))

        brief_list: list[dict] = parse_json(r)

        return {'briefs': brief_list}

    async def _llm_pr_review_plan(self, state: ChatbotAgentState):
        llm = self._llm_loader.get_llm_model()

        simple_chain = ModulePromptFactory(
            StrOutputParser(),
            model=llm,
            name='PR Bot Review',
            partial_variables={
                'pr_patch': state['pr_patch'],
                'custom_instruction': get_custom_instruction(state['custom_instruction'])
            },
            system_prompt_text=PLAN_SYSTEM_PROMPT,
            human_prompt_text=PLAN_HUMAN_PROMPT,
        ).create_chain()

        r = await (simple_chain.with_config({"run_name": "PR Plan"}).ainvoke({}))

        return {'plan': r}

    def create_graph(self):
        g_workflow = StateGraph(ChatbotAgentState)

        g_workflow.add_node('generate_plan_llm_node', self._llm_pr_review_plan)
        g_workflow.add_node('generate_draft_llm_node', self._llm_pr_draft_plan)

        g_workflow.add_node('file_preparation_node', self._file_preparation)
        g_workflow.add_node('file_dependency_path_node', self._llm_file_dependency_path)

        g_workflow.set_entry_point('file_preparation_node')
        g_workflow.add_edge('file_preparation_node', 'file_dependency_path_node')
        g_workflow.add_edge('file_dependency_path_node', 'generate_draft_llm_node')
        g_workflow.add_edge('generate_draft_llm_node', 'generate_plan_llm_node')

        g_workflow.add_edge('generate_plan_llm_node', END)

        g_compile = g_workflow.compile()
        return g_compile

