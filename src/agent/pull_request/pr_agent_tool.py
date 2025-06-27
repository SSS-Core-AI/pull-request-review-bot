def get_custom_instruction(c_instruction: str) -> str:
    if c_instruction == '':
        return ''

    return (f"""[Custom instruction]
Strictly follow the instruction
```
{c_instruction}
```
""")