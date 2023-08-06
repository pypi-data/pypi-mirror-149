import json
from typing import List

from fastapi.logger import logger

from ...models.kernel_variable import KernelVariable
from ...utils import NotebookNode
from ..vars_manager import VarsManager

raw_get_vars_code = """
if (length(find.package('rjson', quiet=TRUE)) < 1) {
    install.packages('rjson')
}
library('rjson')

d1___data <- list()
d1___idx <- 1
for (d1___item in ls()){
    if (d1___item %in% list("d1___data", "d1___idx", "d1___item ", "d1___value", "d1___type", "d1___summary")) {
        next
    }
    d1___summary = get(d1___item)
    d1___value = list(single_value=get(d1___item))
    d1___type = class(d1___value)
    d1___data[[d1___idx]] <- list(name=d1___item, value=d1___value, summary=d1___summary, type=d1___type)
    d1___idx <- d1___idx + 1
}
noquote(rjson::toJSON(d1___data))
rm(d1___data, d1___idx, d1___item, d1___value, d1___type, d1___summary)
"""  # noqa


class RVarsManager(VarsManager):
    def get_vars_code(self) -> str:
        return raw_get_vars_code

    def parse_vars_response(
        self, vars_response: NotebookNode
    ) -> List[KernelVariable]:
        vars: List[KernelVariable] = []
        if "data" not in vars_response:
            return vars
        text = vars_response["data"]["text/plain"].split(" ", 1)[1]
        json_vars = json.loads(text)
        for json_var in json_vars:
            try:
                vars.append(
                    KernelVariable(
                        name=json_var.get("name"),
                        type=json_var.get("type"),
                        # summary=str(json_var.get("summary")),
                        summary=None,
                        # value=str(json_var.get("value"))))
                        value={},
                    )
                )
            except Exception as e:
                logger.debug(
                    f"Exception parsing vars for R kernel: {e}, "
                    f"{json_vars}"
                )
        return vars
