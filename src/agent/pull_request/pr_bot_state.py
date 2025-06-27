from typing import TypedDict
from src.model.pull_request_model import FileModel



class ChatbotAgentState(TypedDict):
    pr_patch: str
    plan: str
    custom_instruction: str

    file_commit_concat_text: str # Concat content of all commit files
    file_dependencies_path_text: str # Only the local import dependency from the commit files
    file_lookup_table: dict[str, FileModel]

