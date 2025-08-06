from src.model.pull_request_model import PullRequestIssueModel
from src.utility.utility_func import get_priority_markdown
import re


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


def split_git_patches(patch_content: str):
    """
    Split a multi-commit git patch into individual text sections.

    Returns a list of individual commit patches as plain text.
    """

    # Split on "From [40-character-hash]" lines
    pattern = r'(?=^From\s+[a-f0-9]{40})'

    patches = re.split(pattern, patch_content, flags=re.MULTILINE)

    # Clean up and return non-empty sections
    return [patch.strip() for patch in patches if patch.strip()]

def git_patches_to_text(patch_contents: list[str]):
    text = ''

    for index, patch in enumerate(patch_contents):
        text += f'''Section index {index}:
{patch}\n\n'''

    return text