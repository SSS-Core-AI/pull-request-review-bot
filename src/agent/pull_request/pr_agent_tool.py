from src.model.pull_request_model import PullRequestIssueModel
from src.utility.utility_func import get_priority_markdown


def get_custom_instruction(c_instruction: str) -> str:
    if c_instruction == '':
        return ''

    return f"""[Instruction]
Strictly follow the instruction
```
{c_instruction}
```\
"""


def get_comment_content(title: str, priority: str, content: str) -> str:
    issue_text = f'''### Issue: {title}
{get_priority_markdown(priority)}

{content}'''

    return issue_text