import json
from typing import List

from fastapi.logger import logger

from ...models.kernel_variable import KernelVariable
from ...utils import NotebookNode
from ..vars_manager import VarsManager

# Copies vars items, creates list of dicts, prints to stdout,
# and then cleans up. Strange var names used to avoid affecting users
# variables.
# Valid python 3 and python 2 code.
raw_get_vars_code = """
import json as __d1_json
from copy import deepcopy as __d1_copy
import traceback as __d1_tb
import sys as __d1_sys

def __d1_humanbytes(B):
       'Return the given bytes as a human friendly KB, MB, GB, or TB string'
       B = float(B)
       KB = float(1024)
       MB = float(KB ** 2) # 1,048,576
       GB = float(KB ** 3) # 1,073,741,824
       TB = float(KB ** 4) # 1,099,511,627,776
    
       if B < KB:
          return '{0} {1}'.format(B,'Bytes' if B > 1 else 'Byte')
       elif KB <= B < MB:
          return '{0:.2f} KB'.format(B/KB)
       elif MB <= B < GB:
          return '{0:.2f} MB'.format(B/MB)
       elif GB <= B < TB:
          return '{0:.2f} GB'.format(B/GB)
       elif TB <= B:
          return '{0:.2f} TB'.format(B/TB)

def __d1_make_multi_dict(row_names, column_names, data):
    if type(column_names) == str:
        column_names = [column_names]
    if type(row_names) == str:
        row_names == [row_names]
    # Make sure the names are strings
    # column_names = tuple(map(lambda x: str(x), column_names))
    # row_names = tuple(map(lambda x: str(x), row_names))
    value = {
        "column_count": len(column_names),
        "row_count": len(row_names),
        "column_names": column_names,
        "row_names": row_names,
        "data": data
    }
    return {"multi_value": value} 
    
def __d1_validate_value(value):
    if list(value.keys()) == ["single_value"]:
        return {"single_value": str(value["single_value"])}
    elif list(value.keys()) == ["multi_value"]:
        val = value['multi_value']
        val['column_names'] = list(map(str, val['column_names']))
        val['row_names'] = list(map(str, val['row_names']))
        # double map through the nested arrays in 'data'
        val['data'] = list(map(lambda x: list(map(str, x)), val['data']))
        return {"multi_value": val} 
    else:
        msg = "Value should be single entry dict with a key of 'single_value' or 'multi_value'."
        msg += f" Found keys: {tuple(value.keys())}"
        raise ValueError(msg)
    
try:
    __d1_vars = []
    for __d1_item in tuple(vars().items()):
        __d1_name = __d1_item[0]
        __d1_obj = __d1_item[1]
        if __d1_name.startswith("__"):
            continue
        __d1_type = type(__d1_obj)
        if __d1_type.__name__ in ['type', 'module', 'function']:
            continue
        
        # check custom values (careful not to call summary / value on the Class object, only on the instances)
        if __d1_type != type and hasattr(__d1_obj, 'jupyter_d1_summary') and callable(getattr(__d1_obj, 'jupyter_d1_summary')):
            __d1_summary = __d1_obj.jupyter_d1_summary()
            if hasattr(__d1_obj, 'jupyter_d1_value') and callable(getattr(__d1_obj, 'jupyter_d1_value')):
                __d1_value = __d1_obj.jupyter_d1_value()
            else:
                __d1_value = None
        # single valued intrinsics
        elif __d1_type.__name__ in ["int", "str", "float", "bool", "complex"]:
            __d1_summary = __d1_obj
            __d1_value = { "single_value": str(__d1_obj) }
        # list
        elif __d1_type.__name__ == "list" or __d1_type.__name__ == "tuple":        
            __d1_summary = f"Length: {len(__d1_obj)}"                
            __d1_data = tuple(map(lambda x: [str(x)], __d1_obj))
            __d1_row_names = list(range(len(__d1_obj)))
            __d1_value = __d1_make_multi_dict(__d1_row_names, __d1_name, __d1_data)
        # dictionary
        elif __d1_type.__name__ == "dict":        
            __d1_summary = f"Length: {len(__d1_obj)}"                
            __d1_data = tuple(map(lambda x: [str(x[0]), str(x[1])], __d1_obj.items()))
            __d1_row_names = list(range(len(__d1_obj)))
            __d1_value = __d1_make_multi_dict(__d1_row_names, ["Key", "Value"], __d1_data)
    
        # numpy 2D array 
        elif __d1_type.__name__ == "ndarray" and __d1_obj.ndim == 2:        
            __d1_summary = f"Size: {__d1_obj.shape[0]}x{__d1_obj.shape[1]}"     \
            + f" Memory: {__d1_humanbytes(__d1_obj.nbytes)}"                
            __d1_data = __d1_obj.tolist()
            __d1_row_names = list(range(__d1_obj.shape[0]))
            __d1_column_names = list(range(__d1_obj.shape[1]))
            __d1_value = __d1_make_multi_dict(__d1_row_names, __d1_column_names, __d1_data)

        # numpy 1D array 
        elif __d1_type.__name__ == "ndarray" and __d1_obj.ndim == 1:        
            __d1_summary = f"Length: {__d1_obj.shape[0]}"     \
            + f" Memory: {__d1_humanbytes(__d1_obj.nbytes)}"                
            __d1_data = tuple(map(lambda x: [str(x)], __d1_obj.tolist()))
            __d1_row_names = list(range(__d1_obj.shape[0]))
            __d1_column_names = __d1_name
            __d1_value = __d1_make_multi_dict(__d1_row_names, __d1_column_names, __d1_data)

        # pandas data frame
        elif __d1_type.__name__ == "DataFrame":        
            __d1_summary = f"Size: {__d1_obj.shape[0]}x{__d1_obj.shape[1]}"     \
                + f" Memory: {__d1_humanbytes(__d1_obj.memory_usage(deep=True).sum())}"                
            __d1_data = __d1_obj.to_numpy().tolist()
            __d1_row_names = tuple(map(lambda x: str(x), __d1_obj.index.to_list()))
            __d1_column_names = __d1_obj.columns.to_list()
            __d1_value = __d1_make_multi_dict(__d1_row_names, __d1_column_names, __d1_data)
        
        # pandas series
        elif __d1_type.__name__ == "Series":        
            __d1_summary = f"Length: {len(__d1_obj)}"                
            __d1_data = tuple(map(lambda x: [str(x)], __d1_obj.to_list()))
            __d1_row_names = tuple(map(lambda x: str(x), __d1_obj.index.to_list()))
            __d1_value = __d1_make_multi_dict(__d1_row_names, __d1_name, __d1_data)
            
        # if all else fails, fall back to single value string representation
        else:
            __d1_summary = str(__d1_obj)
            __d1_value = { "single_value": str(__d1_obj) }
    
        __d1_vars.append({
            "name": __d1_name, 
            "type": __d1_type.__name__, 
            "summary": str(__d1_summary)[:140],        # limit summary length
            "value": __d1_validate_value(__d1_value)
        })
    print(__d1_json.dumps(__d1_vars))
except Exception as e:
    __d1_exc_type, __d1_exc_value, __d1_exc_tb = __d1_sys.exc_info()
    __d1_tb_lines = __d1_tb.format_exception(__d1_exc_type, __d1_exc_value, __d1_exc_tb)
    __d1_vars = [{
        "name": "Introspection Error", 
        "type": type(e).__name__, 
        "summary": str(e),
        "value": { 
            "multi_value": {
                "column_count": 1,
                "row_count": len(__d1_tb_lines),
                "column_names": "Traceback",
                "row_names": list(range(len(__d1_tb_lines))),
                "data": tuple(map(lambda x: [x], __d1_tb_lines))
            }
        }
    }]
    print(__d1_json.dumps(__d1_vars))

for __d1_key in tuple(vars().keys()):
    if __d1_key.startswith("__d1_"):
        del vars()[__d1_key]
del __d1_key
"""  # noqa


class PythonVarsManager(VarsManager):
    def get_vars_code(self) -> str:
        return raw_get_vars_code

    def parse_vars_response(
        self, vars_response: NotebookNode
    ) -> List[KernelVariable]:
        vars = []
        try:
            json_vars = json.loads(vars_response.text)
            for json_var in json_vars:
                vars.append(
                    KernelVariable(
                        name=json_var.get("name"),
                        type=json_var.get("type"),
                        value=json_var.get("value"),
                        summary=json_var.get("summary"),
                    )
                )
        except Exception as e:
            logger.debug(
                f"Exception parsing vars for python kernel: {e}, "
                f"{vars_response.text}"
            )
        return vars
