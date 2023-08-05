from typing import Any, Mapping


def prepare_params(params: Mapping[str, Any]):
    new_params = {}
    for key, value in params.items():
        if type(value) is list:
            new_params[key] = ",".join(map(str, value))
        else:
            new_params[key] = value
    return new_params
