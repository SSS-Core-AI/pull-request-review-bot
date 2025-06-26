from typing import TypedDict


class ChatbotAgentState(TypedDict):
    pr_patch: str
    plan: str
    custom_instruction: str
    file_dependencies_text: str
    file_dependencies_list: list[str]