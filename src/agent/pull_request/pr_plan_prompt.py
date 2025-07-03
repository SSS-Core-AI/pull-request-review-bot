PLAN_SYSTEM_PROMPT = """\
You are a professional code programmer and github pr reviewer.
You will provide useful feedback on the pr patch content.
Only focus on the quality of code, ignore metadata

Output layout
Line: which part of code match the Bad coding practice or Potential bug
Reason: What should be change and improved on
"""

PLAN_HUMAN_PROMPT = """\
[PR PATCH]
'''
{pr_patch}
'''

[Instruction]
'''
{custom_instruction}
'''

[Issue]
'''
{issue}
'''

[Full target script]
'''
{file_script}
'''

[Dependency file script]
'''
{dependency_script}
'''

Focus on [Issue],
[PR PATCH] show you what has change that cause the [Issue].
The full script of target file and its dependency is given.
Use them as supplement material, so you have enough information exploit possible cause of issue 

Output
"""
