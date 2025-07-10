def get_custom_instruction(c_instruction: str) -> str:
    if c_instruction == '':
        return ''

    return (f"""[Instruction]
Strictly follow the instruction
```
{c_instruction}
```\
""")