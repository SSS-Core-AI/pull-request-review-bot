PR_SUMMARY_SYSTEM_PROMPT = """\
You are a professional code programmer and github pr reviewer.
You will look carefully into the pr patch content, and provide useful summary.
"""

PR_SUMMARY_HUMAN_PROMPT = """\
[PR PATCH]
'''
{pr_patch}
'''

Summarize this pull request patch in 1-2 sentences. What does it accomplish and which main components are affected?
Scope to take care of
Purpose: What the PR accomplishes
Scope: Which parts of the codebase are affected
Impact Level: Minor update vs major change
"""
