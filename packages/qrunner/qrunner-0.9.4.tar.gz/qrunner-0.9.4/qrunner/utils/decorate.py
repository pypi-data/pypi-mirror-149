# @Time    : 2022/2/22 10:37
# @Author  : kang.yang@qizhidao.com
# @File    : decorate.py
import json
import os

import allure
import pytest
import inspect as sys_inspect


def feature(text):
    return allure.feature(text)


def story(text):
    return allure.story(text)


# 兼容历史版本
def module(text):
    return allure.story(text)


def title(text):
    return allure.title(text)


def data(*args, **kwargs):
    return pytest.mark.parametrize(*args, **kwargs)


# 有空把文件装饰器补上
def file_data(data_key=None, file_name=None):
    # 获取被装饰方法的目录
    stack_t = sys_inspect.stack()
    ins = sys_inspect.getframeinfo(stack_t[1][0])
    file_dir = os.path.dirname(os.path.abspath(ins.filename))
    parent_dir = os.path.dirname(file_dir)
    parent_dir_dir = os.path.dirname(parent_dir)
    parent_dir_dir_dir = os.path.dirname(parent_dir_dir)

    # 判断当前、父目录、爷目录、太爷爷目录下的test_data目录下是否有file_name文件
    path_list = [file_dir, parent_dir, parent_dir_dir, parent_dir_dir_dir]
    file_path = None
    full_list = []
    for _path in path_list:
        full_path = os.path.join(_path, 'test_data', file_name)
        full_list.append(full_path)
        # print(full_path)
        if os.path.isfile(full_path) is True:
            file_path = full_path
            break
    if file_path is None:
        raise Exception(f"can not found {file_name} in {full_list}")

    # 根据文件路径以及key获取文件中的数据，暂时只支持json文件
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    content = json_data[data_key]
    return data(data_key, content)
