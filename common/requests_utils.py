# -*- coding: utf-8 -*-
# @Time : 2021/5/26 10:36
# @Author : MIGE
# @File : requests_utils.py
'''
封装不是一蹴而就的
'''
import json
import traceback
import jsonpath as jsonpath
import requests
import re
from common.common_utils import read_config_yaml, read_extract_yaml
from common.common_utils import write_extract_yaml
from debugtalk import Debug_Talk
from common.logger_utils import write_log, error_log


class Requests_Utils:
    '''
    定义一个发送请求的类
    方法有：
    analysis_yaml： 对读取yaml用例文件得到的数据进行分析，得到 method、header、data、files等数据
    send_Requests： 根据得到的数据发送请求
    validate_result： 根据返回的数据断言结果
    '''
    # 初始化的构造方法
    def __init__(self):
        # 初始化基础路径
        self.base_url = read_config_yaml('base', 'base_url')
        # 初始化请求头 dict格式
        self.last_headers = {}
        # 初始化data
        self.last_data = {}
        # 初始化请求方式
        self.last_method = ""

    def analysis_yaml(self, caseinfo):
        '''
        对读取yaml用例文件得到的数据进行分析
        :param caseinfo: 读取yaml用例文件得到的caseinfo(已经进行数据驱动) 类型为（dict）
        :return:
        '''
        try:
            # 判断：name，request，validate 这三个关键字是否存在（caseinfo是个字典 ，这三个关键字是字典里的key，判断字典有没有这三个key）
            if 'name' in dict(caseinfo).keys() and 'request' in dict(caseinfo).keys() and 'validate' in dict(
                    caseinfo).keys():
                # 判断request下的二级关键字 method，url，data是否存在
                if jsonpath.jsonpath(caseinfo, '$..method') and jsonpath.jsonpath(caseinfo, '$..url') and jsonpath.jsonpath(caseinfo, '$..data'):
                    # 判断请求头和文件是否存在
                    headers, files = None, None
                    if jsonpath.jsonpath(caseinfo, '$..headers'):
                        headers = caseinfo['request']['headers']
                    if jsonpath.jsonpath(caseinfo, '$..files'):
                        new_file_dict = {}
                        for key, value in dict(caseinfo['request']['files']).items():
                            new_file_dict[key] = open(r"" + value, 'rb')
                        files = new_file_dict
                        # files = caseinfo['request']['files']
                        # files = open(caseinfo['request']['files'], 'rb')
                    # 收集日志
                    write_log('-' * 30 + "接口请求开始" + '-' * 30)
                    write_log("接口名称：%s" % caseinfo['name'])
                    write_log("接口请求方式：%s" % caseinfo['request']['method'])
                    write_log("接口路径：%s" % caseinfo['request']['url'])
                    write_log("接口数据：%s" % caseinfo['request']['data'])
                    # write_log("请求文件：%s" % caseinfo['request']['files'])
                    # 发送请求
                    res = self.send_Requests(method=caseinfo['request']['method'],
                                             url=caseinfo['request']['url'],
                                             headers=headers,
                                             data=caseinfo['request']['data'],
                                             files=files)
                    # 获取返回值和返回状态码
                    expected_result = caseinfo['validate']
                    text_result = res.text
                    actual_result = res.json()
                    status_code = res.status_code
                    # 调用断言方法进行断言
                    self.validate_result(expected_result, actual_result, status_code)

                    # 封装提取变量（json提取器，正则表达式提取器）
                    # 正则表达式提取器提取变量
                    if jsonpath.jsonpath(caseinfo, '$..extract'):
                        for key, value in dict(caseinfo['extract']).items():
                            if '(.+?)' in value or '(.*?)' in value:
                                obj = re.search(value, res.text)
                                if obj:
                                    data_dict = {key: obj.group(1)}
                                    write_extract_yaml(data_dict)
                            else:
                                # json提取器提取变量
                                temp_data = jsonpath.jsonpath(res.json(), '$..%s' % value)
                                if temp_data:
                                    data_dict = {key: temp_data[0]}
                                    write_extract_yaml(data_dict)

                else:
                    error_log("一级关键字request下，url，method，data必填")
                    # print("关键字request下，url，method，data必填")
            else:
                error_log("一级关键字name，request，validate必填")
                # print("一级关键字name，request，validate必填")
        except Exception as e:
            error_log("读取yaml用例文件得到的数据进行分析出错，异常信息：%s" % str(traceback.format_exc()))
            raise e

    def validate_result(self, expected_result, actual_result, status_code):
        '''
        断言结果
        :param expected_result: 预期结果 list类型
        :param actual_result: 实际结果  dict类型
        :return: 断言成功与否的标记
        '''
        write_log("预期结果：%s" % expected_result)
        write_log("实际结果：%s" % actual_result)
        try:
            write_log('-' * 20 + "断言开始" + '-' * 20)
            flag = 0
            if expected_result and isinstance(expected_result, list):
                for expect in expected_result:
                    for key, value in dict(expect).items():
                        if key == 'equals':
                            for assert_key, assert_value in dict(value).items():
                                if assert_key == 'status_code':
                                    if status_code != assert_value:
                                        flag += 1
                                        error_log("断言失败，返回的状态码有误")
                                        # print("断言失败，返回的状态码有误")
                                    else:
                                        write_log("状态码断言成功.......")
                                        # print("状态码断言成功......")
                                else:
                                    all_value = jsonpath.jsonpath(actual_result, '$..%s' % assert_key)
                                    if all_value:
                                        if assert_value not in all_value:
                                            flag += 1
                                            error_log("断言失败")
                                            # print("断言失败，")
                                        else:
                                            write_log("业务断言成功，业务值相等.")
                                            # print("业务断言成功，业务值相等.")
                                    else:
                                        flag += 1
                                        error_log("断言失败，断言的key不存在")
                                        # print("断言失败，断言的key不存在")

                        elif key == 'contains':
                            if value not in json.dumps(actual_result):
                                flag += 1
                                error_log("断言失败，实际结果中不包含字符串" + value)
                                # print("断言失败，实际结果中不包含字符串" + value)
                            else:
                                write_log("业务断言成功，包含断言字符串" + value)
                                # print("业务断言成功，包含断言字符串" + value)
                        else:
                            error_log("不支持的断言方式")
                            # print("不支持的断言方式")
            assert flag == 0
            write_log('-' * 20 + "断言结束" + '-' * 20)
            write_log('-' * 30 + "接口请求结束" + '-' * 30 + "\n")
        except Exception as e:
            error_log("断言出错，异常信息：%s" % str(traceback.format_exc()))
            write_log('-' * 30 + "接口请求结束" + '-' * 30 + "\n")
            raise e

    def send_Requests(self, method, url, headers=None, data=None, files=None):
        '''
        封装的统一的接口的请求方式
        :param method:
        :param url:
        :param headers:
        :param data:
        :param files:
        :return:
        data：text和简单的只有键值对的字典，如果是复杂的字典（多层嵌套）需要通过json.dumps()转化成文本格式，再传输
        json：字典格式（dict）
        post中 data和json的区别，data可以传简单的字典格式（键值对）
        json传的是复杂的字典(dict)格式（多层级），如果用data来传这种复杂的字典(dict)格式，
        那必须把复杂的dict先json.dumps()转换为一个文本，再传给data
        '''
        # 处理url
        try:
            for i in range(1, url.count("{{") + 1):
                if '{{' in url and '}}' in url:
                    start_index = url.index('{{')
                    end_index = url.index('}}', start_index)
                    # print(start_index, end_index)
                    old_value = url[start_index: end_index + 2]
                    # print(old_value)
                    new_value = read_extract_yaml(old_value[2: -2])
                    # print(new_value)
                    url = url.replace(old_value, new_value)
                    # print(url)
            self.last_url = self.base_url + url
            # 把get Get GET都转化成小写---无论传入什么，都转化成小写
            self.last_method = str(method).lower()
            # 处理data参数--0和None表示False
            if data and isinstance(data, dict):
                # 处理热加载数据
                text_data = json.dumps(data)
                if '${' in text_data and '}' in text_data:
                    start_index = text_data.index('${')
                    end_index = text_data.index('}', start_index)
                    old_value = text_data[start_index: end_index + 1]
                    function_name = old_value[2: int(old_value.index('('))]
                    new_random_number = getattr(Debug_Talk(), function_name)()
                    text_data = text_data.replace(old_value, str(new_random_number))
                data = json.loads(text_data)
                # 处理接口关联取值
                for key, value in data.items():
                    if str(value).startswith('{{') and str(value).endswith('}}'):
                        data[key] = read_extract_yaml(str(value)[2: -2])
                # 如果不是get请求，那么通过json.dumps()转换成json格式的字符串
                if not self.last_method == 'get':
                    self.last_data = json.dumps(data)
                else:
                    self.last_data = data
            # 处理请求头headers的参数提取
            if headers and isinstance(headers, dict):
                for key, value in headers.items():
                    if str(value).startswith('{{') and str(value).endswith('}}'):
                        headers[key] = read_extract_yaml(str(value)[2: -2])
                self.last_headers = headers
            # 判断请求方式
            res = None
            if self.last_method == "get":
                res = self.get(self.last_url, self.last_headers, self.last_data)
            elif self.last_method == "post":
                # 如果传的的是字典格式（dict），那么需要使用json.dumps()序列化
                res = self.post(self.last_url, self.last_headers, self.last_data, files)
            elif self.last_method == "put":
                res = self.put(self.last_url, self.last_headers, self.last_data)
            elif self.last_method == "delete":
                res = self.dels(self.last_url, self.last_headers, self.last_data)
            else:
                error_log("暂不支持此请求方式：%s" % self.last_method)
                # print("暂不支持此请求方式：%s" % self.last_method)
            print("响应信息-文本格式", res.text)
            print("响应信息-JSON格式", res.json())
            return res
        except Exception as e:
            error_log("发送请求出错，异常信息：%s" % str(traceback.format_exc()))
            raise e

    def get(self, url, headers, params):
        res = requests.get(url, headers=headers, params=params)
        return res

    def post(self, url, headers, data, files):
        res = requests.post(url, headers=headers, data=data, files=files)
        return res

    def put(self, url, headers, data):
        res = requests.put(url, data=data, headers=headers)
        return res

    def dels(self, url, headers, data):
        res = requests.delete(url, data=data, headers=headers)
        return res


if __name__ == '__main__':
    pass