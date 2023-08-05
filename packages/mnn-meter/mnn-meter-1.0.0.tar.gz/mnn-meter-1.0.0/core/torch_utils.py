# _*_ coding: utf-8 _*_
"""
Time:     2022-05-01 17:23
Author:   Haolin Yan(XiDian University)
File:     torch_utils.py
"""
import importlib
import copy


def import_module(pkg):
    return importlib.import_module(pkg)


def generate_param_list(kwargs):
    cfg_list = []

    def generate_param(param, **kwargs):
        for i, (k, v) in enumerate(param.items()):
            if v or k == "input_shape":
                continue
            table = kwargs[k]
            for j, ele in enumerate(table):
                param[k] = ele
                param_ = copy.deepcopy(param)
                if i == 0:
                    param_["input_shape"] = kwargs["input_shape"][j]
                generate_param(param_, **kwargs)
            return 0
        cfg_list.append(param)

    param = dict((n, None) for n in kwargs.keys())
    generate_param(param, **kwargs)
    return cfg_list


def remove_(str):
    last = ""
    new_str = ""
    for s in str:
        if s == last:
            continue
        new_str += s
        last = s
    return new_str


def replace(str):
    str = str.replace("(", "-").replace(")", "-").replace(",", "-").replace(" ", "")
    return remove_(str)
