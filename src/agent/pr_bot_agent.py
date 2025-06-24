import os

from langchain_core.output_parsers import StrOutputParser
from langgraph.constants import END
from langgraph.graph import StateGraph

from src.agent.pr_bot_state import ChatbotAgentState
from src.agent.prompt_static import PLAN_SYSTEM_PROMPT, PLAN_HUMAN_PROMPT
from src.utility.model_loader import ILLMLoader, GPT41
from src.utility.module_prompt_factory import ModulePromptFactory

class PRBotAgent:
    def __init__(self, llm_loader: ILLMLoader, ):
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

    def _generate_pr_review_plan(self, state: ChatbotAgentState):
        llm = self._llm_loader.get_llm_model()

        simple_chain = ModulePromptFactory(
            StrOutputParser(),
            model=llm,
            name='Learning Objectives',
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

        g_workflow.add_node('generate_plan_node', self._generate_pr_review_plan)

        g_workflow.set_entry_point('generate_plan_node')
        g_workflow.add_edge('generate_plan_node', END)

        g_compile = g_workflow.compile()
        return g_compile

