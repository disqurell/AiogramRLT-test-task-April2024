import json
from .strings import INVALID_MESSAGE


def validator(input_data: str):
    if not input_data:
        return INVALID_MESSAGE

    try:
        data_dict = json.loads(input_data)
    except json.JSONDecodeError:
        return INVALID_MESSAGE

    return data_dict
