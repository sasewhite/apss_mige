#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   common_utils.py    
@Contact :   sasewhite@live.com
@License :   (C)Copyright 2017-2021, 114S-342t-3Y

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/5/27 15:58   Mige      1.0         None
'''
import csv

'''
不能写硬编码！！！！！！！！
'''
import os

import yaml


# 获取到项目路径
def get_object_path():
    return os.path.realpath(__file__).split('common')[0]


# 读取配置文件yaml----config.yaml
def read_config_yaml(one_node, tow_node):
    with open(get_object_path() + "config.yml", 'r', encoding='utf-8') as f:
        value = yaml.load(f.read(), yaml.FullLoader)
        return value[one_node][tow_node]


# 读取extract文件yaml----config.yaml
def read_extract_yaml(key):
    with open(get_object_path() + "extract.yaml", 'r', encoding='utf-8') as f:
        value = yaml.load(f.read(), yaml.FullLoader)
        return value[key]


# 写入extract文件yaml----config.yaml
def write_extract_yaml(data_dict):
    with open(get_object_path() + "extract.yaml", 'a', encoding='utf-8') as f:
        yaml.dump(data_dict, stream=f, allow_unicode=True)


# 清空extract文件的yaml
def clear_extract_yaml():
    with open(get_object_path() + "extract.yaml", 'w', encoding='utf-8') as f:
        f.truncate()


# 读取数据csv文件的方法
def read_csv_data(path):
    data_list = []
    with open(get_object_path() + path, 'r', encoding='utf-8') as f:
        data = csv.reader(f)
        for i in data:
            data_list.append(i)
    return data_list


if __name__ == '__main__':
    print(read_csv_data(r"data/get_token_data.csv"))
    raw =  read_testcase_yaml(r"testcase/get_token.yaml")