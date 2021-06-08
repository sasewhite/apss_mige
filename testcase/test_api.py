#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_api.py    
@Contact :   sasewhite@live.com
@License :   (C)Copyright 2017-2021, 114S-342t-3Y

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/5/28 15:13   Mige      1.0         None
'''
import json
import jsonpath
import pytest
from common.paramters_utils import read_testcase_yaml
from common.requests_utils import Requests_Utils


'''
作用：专门用来读取yaml文件（读取yaml测试用例）
'''


class Test_Api:

    # read_testcase_yaml得到的是一个字典列表[{},{},{}]，caseinfo是一个字典，其实是列表中的某个元素（字典）每次传一个dict进去
    @ pytest.mark.parametrize('caseinfo', read_testcase_yaml('testcase/get_token.yaml'))
    def test_get_token(self, caseinfo):
        Requests_Utils().analysis_yaml(caseinfo)
        # print(caseinfo)
        # print(caseinfo['name'])
        # print(caseinfo['request']['method'])
        # print(caseinfo['request']['url'])
        # print(caseinfo['request']['data'])
        # print(type(caseinfo))
        # print(caseinfo.keys())
    # @ pytest.mark.parametrize('caseinfo', read_testcase_yaml('testcase/edit_flag.yaml'))
    # def test_edit_flag(self, caseinfo):
    #     Requests_Utils().analysis_yaml(caseinfo)
    #
    # @ pytest.mark.parametrize('caseinfo', read_testcase_yaml('testcase/select_flag.yaml'))
    # def test_select_flag(self, caseinfo):
    #     Requests_Utils().analysis_yaml(caseinfo)
    #
    # @ pytest.mark.parametrize('caseinfo', read_testcase_yaml('testcase/file_upload.yaml'))
    # def test_file_upload(self, caseinfo):
    #     Requests_Utils().analysis_yaml(caseinfo)

