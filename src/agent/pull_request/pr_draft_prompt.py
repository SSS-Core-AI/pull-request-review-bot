PR_DRAFT_SYSTEM_PROMPT = """\
You are a professional code programmer and github pr reviewer.
You will provide useful feedback on the pr patch content.
Only focus on the code itself, ignore metadata

Given a pull request patch, the commited files name and its dependency files name
Your job here is to point out the possible issue fit the criteria\
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

Focus on the potential issue from [PR PATCH], and used [File and its dependency] as supplement materials

Output the dependency file path in the format of json array as below
```json
[
    {{
        "pr_patch": "The section on [PR PATCH], that has issue",
        "issue": "a short explanation on what the issue is",
        "file_path": "the path of main file",
        "dependency_paths": [a list of dependency file paths, worth a look]
    }}
]
```\
"""
