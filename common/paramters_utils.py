#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   paramters_utils.py    
@Contact :   sasewhite@live.com
@License :   (C)Copyright 2017-2021, 114S-342t-3Y

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/2 8:58   Mige      1.0         None
'''
import traceback

'''
数据驱动的处理方法！！！！
'''

import json
import jsonpath
import yaml
from common.common_utils import get_object_path, read_csv_data
from common.logger_utils import write_log, error_log


# 读取测试用例testcase文件yaml----测试用例.yaml
def read_testcase_yaml(testcase_yaml_name):
    '''
    读取测试用例yaml文件，得到一个测试用例的字典列表----[{}, []]
    如果列表的字典中有parameters关键字，则进行csv数据替换，（数据驱动），得到一个测试用例的字典列表-----[{}, {}, {}]
    :param testcase_yaml_name:
    :return: new_caseinfo ---字典列表  [{}, {}, {}]
    '''
    with open(get_object_path() + testcase_yaml_name, 'r', encoding='utf-8') as f:
        value = yaml.load(f.read(), yaml.FullLoader)
    print()
    print("读取到的yaml数据为：%s" %value)
    print("读取到的yaml数据类型为：%s" %type(value))
    if len(value) >= 2:
        return value
    else:
        if jsonpath.jsonpath(*value, '$.parameters'):
            new_caseinfo = analysis_paramters(*value)
            return new_caseinfo
        else:
            return value


def analysis_paramters(caseinfo):
    '''
    -数据驱动-
    如果从测试用例yaml文件中读取到的caseinfo中存在一级标签parameters，
    那就用csv文件中的数据替换caseinfo中的变量。
    :param caseinfo: dict类型
    :return: new_caseinfo --替换后的caseinfo  字典的列表 [{},{},{}]
    '''
    try:
        if jsonpath.jsonpath(caseinfo, '$.parameters'):
            for key, value in dict(caseinfo['parameters']).items():
                # 把字典格式的caseinfo转化成字符串
                text_caseinfo = json.dumps(caseinfo)
                # 把以‘-’隔开的key转换成list
                key_list = str(key).split('-')
                # 判断csv文件中的key和数据的长度一致
                length_flag = True
                csv_data = read_csv_data(value)
                print("读取到的csv数据为：%s" % csv_data)
                print("读取到的csv数据类型为：%s" % type(csv_data))
                # 提取第一行的数据
                one_row = csv_data[0]
                for row in csv_data:
                    if len(one_row) != len(row):
                        length_flag = False
                        break
                # 替换yaml文件中的$csv{}格式数据
                new_caseinfo = []
                if length_flag:
                    for x in range(1, len(csv_data)):  # X是横坐标
                        temp_caseinfo = text_caseinfo  # 初始化，保持text_caseinfo的值不变
                        for y in range(0, len(csv_data[x])):
                            if csv_data[0][y] in key_list:
                                temp_caseinfo = temp_caseinfo.replace("$csv{" + csv_data[0][y] + "}", csv_data[x][y])
                        new_caseinfo.append(json.loads(temp_caseinfo))
                print("替换后的new_caseinfo为：%s" %new_caseinfo)
                print("new_caseinfo的格式为", type(new_caseinfo))
                for raw in new_caseinfo:
                    print("数据驱动-用csv中数据替换后的caseinfo数据--字典（dict）格式", raw)
            return new_caseinfo
    except Exception as e:
        error_log("分析paramters参数化出错，异常信息：%s" % str(traceback.format_exc()))
        raise e
    





if __name__ == '__main__':
    read_testcase_yaml()