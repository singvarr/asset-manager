import os
from typing import Iterable


def check_required_env_variables(required_env_variables: Iterable[str]):
    for variable in required_env_variables:
        if variable not in os.environ:
            raise Exception(f"Variable {variable} is missing in .env")
