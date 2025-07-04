import re
from typing import Literal

import json_repair


def parse_block(code: str, raw_message: str) -> str:
    try:
        regex_sympy = r'```{code}(?:.|\n)*?```'
        regex_sympy = regex_sympy.replace('{code}', code)

        sympy_codes: list[str] = re.findall(regex_sympy, raw_message)

        raw_llm_msg: str = raw_message

        if len(sympy_codes) > 0:
            raw_llm_msg: str = sympy_codes[0]

        raw_llm_msg = raw_llm_msg.replace(f'```{code}', '')
        raw_llm_msg = raw_llm_msg.replace('```', '')

        return raw_llm_msg
    except Exception as e:
        print(e)

    return raw_message


def parse_json(raw_message: str) -> dict | list:
    try:
        return json_repair.loads(parse_block('json', raw_message))
    except Exception as e:
        print('parse_json fail to parse ', e)
        raise e


def get_priority_markdown(priority: Literal['high', 'medium', 'low']):
    match priority:
        case 'high':
            return '![High Priority](https://img.shields.io/badge/Priority-High-red)'
        case 'medium':
            return '![Medium Priority](https://img.shields.io/badge/Priority-Medium-orange)'
        case _:
            return '![Low Priority](https://img.shields.io/badge/Priority-Low-green)'
