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


def get_comment_content(pull_request_model: PullRequestIssueModel) -> str:
    issue_text = f'''### Issue: {pull_request_model.title}
    {get_priority_markdown(pull_request_model.priority)}

    {pull_request_model.content}'''

    print('get_comment_content', issue_text)

    return issue_text