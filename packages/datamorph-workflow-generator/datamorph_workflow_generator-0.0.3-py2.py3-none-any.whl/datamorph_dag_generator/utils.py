import ast
import importlib.util
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Any


def load_JSON_file(fname):
    """
    load JSON file in the given path
    :param fname:
    :return:
    """
    with open(fname, "r") as f:
        data = json.load(f)
    return data

def remove_key(dictItem, key):
    """
    removes key from the dict object if key is present
    :param dictItem: dictionary object to remove key from
    :param key: string key name
    :return:
    """
    if key in dictItem:
        r = dict(dictItem)
        del r[key]
        return r
    else:
        return dictItem

def remove_keys(dictItem, keys):
    """
    removes key from the dict object if key is present
    :param dictItem: dictionary object to remove key from
    :param keys: list of string key name
    :return:
    """
    for key in keys:
        if key in dictItem:
            del dictItem[key]


def check_dict_key(item_dict: Dict[str, Any], key: str) -> bool:
    """
    Check if the key is included in given dictionary, and has a valid value.
    :param item_dict: a dictionary to test
    :type item_dict: Dict[str, Any]
    :param key: a key to test
    :type key: str
    :return: result to check
    :type: bool
    """
    return bool(key in item_dict and item_dict[key] is not None)


def load_json_config_file(config_file_path: str):
    """
    load json config file, example with workflow and variables attribute.
    substitute ${VAR} with its value from the variables key value pair.
    variables may or may not be provided.
    {
        "variables":{
           "ENV1":"value1",
           "ENV2":"value2"
        }
        "workflow": [
        "properties": {
            "parm1": 8000,
            "parm2": "${ENV1}",
            "parm3": "${ENV2}"
        }
        ]
    }
    :param config_file_path:
    :return:
    """

    def _substitute_in_dict(d,variables):
        for key in d.keys():
            v = d.get(key)
            if isinstance(v, str):
                m = re.match('\${(\w+)}', v)
                if m:
                    val_name=m.group(1)
                    env_val = variables.get(val_name)
                    d[key] = env_val
            elif isinstance(v, dict):
                _substitute_vars(v, variables)

    def _substitute_vars(d, variables):
        if isinstance(d,list):
            for each in d:
                _substitute_in_dict(each, variables)
        else:
            _substitute_in_dict(d, variables)


    if os.path.isfile(config_file_path):
        with open(config_file_path, 'r') as f:
            app_config = json.load(f)
            workflow = app_config["workflow"]
            if check_dict_key(app_config,"variables"):
                variables = app_config["variables"]
                _substitute_vars(workflow, variables)

            return app_config
    else:
        raise Exception('Configuration file not found: '.format(config_file_path))


def get_python_callable(python_callable_name, python_callable_file):
    """
    Uses python filepath and callable name to import a valid callable for use in PythonOperator
    :param python_callable_name:
    :param python_callable_file:
    :return:
    """
    python_callable_file = os.path.expandvars(python_callable_file)

    if not os.path.isabs(python_callable_file):
        raise Exception("`python_callable_file` must be absolute path")

    python_file_path = Path(python_callable_file).resolve()
    module_name = python_file_path.stem
    spec = importlib.util.spec_from_file_location(module_name, python_callable_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[module_name] = module
    python_callable = getattr(module, python_callable_name)

    return python_callable
