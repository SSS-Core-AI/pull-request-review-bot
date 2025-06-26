from langchain_core.output_parsers import StrOutputParser
from langgraph.constants import END
from langgraph.graph import StateGraph

from src.agent.file_crawler.file_crawler_prompt import FILE_CRAWLER_SYSTEM_PROMPT, FILE_CRAWLER_HUMAN_PROMPT
from src.agent.pull_request.pr_bot_state import ChatbotAgentState
from src.agent.pull_request.prompt_static import PLAN_SYSTEM_PROMPT, PLAN_HUMAN_PROMPT
from src.utility.model_loader import ILLMLoader
from src.utility.module_prompt_factory import ModulePromptFactory
from src.utility.utility_func import parse_json


class PRBotAgent:
    def __init__(self, llm_loader: ILLMLoader):
        self._llm_loader = llm_loader

    def _get_custom_instruction(self, c_instruction: str) -> str:
        if c_instruction == '':
            return ''

        return (f"""[Custom instruction]
Strictly follow the instruction
```
{c_instruction}
```
""")

    def _generate_file_crawler_agent(self, state: ChatbotAgentState):
        llm = self._llm_loader.get_llm_model()
        print('_generate_file_crawler_agent', state['file_dependencies_text'])

        simple_chain = ModulePromptFactory(
            StrOutputParser(),
            model=llm,
            name='File crawler',
            system_prompt_text=FILE_CRAWLER_SYSTEM_PROMPT,
            human_prompt_text=FILE_CRAWLER_HUMAN_PROMPT,
        ).create_chain()

        r = simple_chain.with_config({"run_name": "File crawler"}).invoke({'file_dependencies_text': state['file_dependencies_text']})
        dependencies_list = parse_json(r)

        return {'file_dependencies_list': dependencies_list}

    def _generate_pr_review_plan(self, state: ChatbotAgentState):
        llm = self._llm_loader.get_llm_model()

        simple_chain = ModulePromptFactory(
            StrOutputParser(),
            model=llm,
            name='PR Bot Review',
            partial_variables={
                'pr_patch': state['pr_patch'],
                'custom_instruction': self._get_custom_instruction(state['custom_instruction'])
            },
            system_prompt_text=PLAN_SYSTEM_PROMPT,
            human_prompt_text=PLAN_HUMAN_PROMPT,
        ).create_chain()

        r = simple_chain.with_config({"run_name": "PR Plan"}).invoke({})

        return {'plan': r}

    def create_graph(self):
        g_workflow = StateGraph(ChatbotAgentState)

        g_workflow.add_node('generate_plan_llm_node', self._generate_pr_review_plan)
        g_workflow.add_node('file_crawler_llm_node', self._generate_file_crawler_agent)

        g_workflow.set_entry_point('file_crawler_llm_node')
        g_workflow.add_edge('file_crawler_llm_node', 'generate_plan_llm_node')
        g_workflow.add_edge('generate_plan_llm_node', END)

        g_compile = g_workflow.compile()
        return g_compile

