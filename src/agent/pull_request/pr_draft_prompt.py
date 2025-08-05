from src.agent.pull_request.pr_plan_prompt import CODE_REVIEW_RULE

PR_DRAFT_SYSTEM_PROMPT = f"""\
You are a professional code programmer and github pr reviewer.
You will provide useful feedback on the pr patch content.
Only focus on the code itself, ignore metadata

Given a pull request patch, the commited files name and its dependency files name
Your job here is to point out the possible issue fit the criteria

[Code review rule]
'''
{CODE_REVIEW_RULE}
'''
"""

PR_DRAFT_HUMAN_PROMPT = """\
[Summary of patch]
'''
{short_summary}
'''

[PR PATCH]
'''
{pr_patch}
'''

[File and its dependency]
'''
{committed_file_and_dependency}
'''

[Evaluation Criteria]
'''
{custom_instruction}
'''

[How to set the line_number]
'''
Rule 1: If the file is delete, set the line_number to -1
Rule 2: If the issue is a suggestion / improvement, not a coding bugs, set the line_number to -1
Rule 3: If the issue is too huge, can not start from specific line, set the line_number to -1

In short, only set line_number, when you are absolutely sure where the line number locate, or else just set it to negative one.
'''

Focus on the potential issue from [PR PATCH], and used [File and its dependency] as supplement materials
priority 'none' means this issue is not important, we shouldn't tackle on it

Output the dependency file path in the format of json array as below
```json
[
    {{
        "pr_patch": "The section on [PR PATCH], that has issue",
        "title": "The unique title for this issue",
        "issue": "a explanation on what the issue is and what Code review rule it break",
        "priority": "how serious is the issue, categorize into 'high', 'medium', 'low' and 'none' only",
        "file_path": "the path of main file",
        "dependency_paths": [a list of dependency file paths, worth a look],
        "line_number": int type indicate to issue line number on pr_patch
    }}
]
```\
"""
