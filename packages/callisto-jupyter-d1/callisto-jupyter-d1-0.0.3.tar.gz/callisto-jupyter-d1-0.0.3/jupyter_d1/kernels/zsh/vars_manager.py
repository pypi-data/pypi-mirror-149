from typing import List

from fastapi.logger import logger

from ...models.kernel_variable import KernelVariable
from ...utils import NotebookNode
from ..vars_manager import VarsManager

raw_get_vars_code = """
env
"""  # noqa


class ZshVarsManager(VarsManager):
    def get_vars_code(self) -> str:
        return raw_get_vars_code

    def parse_vars_response(
        self, vars_response: NotebookNode
    ) -> List[KernelVariable]:
        vars = []
        try:
            line = vars_response.text.strip()
            name, value = line.split("=", 1)

            vars.append(
                KernelVariable(
                    name=name,
                    type=None,
                    value={"single_value": value},
                    summary=value,
                )
            )
        except Exception as e:
            logger.debug(
                f"Exception parsing var for zsh kernel: {e}, "
                f"{vars_response.text}"
            )
        return vars
