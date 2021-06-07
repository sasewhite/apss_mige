#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   sends.py
@Contact :   sasewhite@live.com
@License :   (C)Copyright 2017-2021, 114S-342T-3Y

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/5/25 20:32   Mige       1.0          None
'''
import json
import os
import re
import time
import requests
from common.common_utils import write_extract_yaml, read_extract_yaml
from common.requests_utils import Requests_Utils


class Test_Sends:

    # access_token = ""
    # csrf_token = ""
    # phpwind_cookie = ""


    def test_get_token (self):
        '''
        获取接口统一鉴权码token接口 获得access_token接口
        :return:
        '''
        url = r"/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": "wxcffb4fed03363e2d",
            "secret": "dc77b17bd2010a2d36b802ee6a6cf143"
        }
        # res = requests.get(url,params=params)
        #直接用统一的接口调用的方式
        res = Requests_Utils().send_Requests('get', url=url, data=params)
        # print(res.text)
        return_value = res.json()
        #把提取的access_token写入yaml文件（dict或者dict的列表）
        extract_dict = {"access_token": return_value["access_token"]}
        write_extract_yaml(extract_dict)
        # print(return_value,type(return_value))                #打印返回的数据，格式：字典格式
        # print(res.content,type(res.content))              #打印返回的数据，格式：字节类型
        # print(res.text,type(res.text))                    #打印返回的数据，格式：字符串格式
        # print(res.status_code)                            #打印接口返回的状态码
        # print(res.headers,type(res.headers))              #打印响应头
        # print(res.headers.get("Connection"))
        # print(res.apparent_encoding)                      #打印编码格式

    def test_get_flag (self):
        '''
        获取公众号已创建的标签接口
        :return:
        '''
        url = r"/cgi-bin/tags/get"
        params = {
            "access_token": "${access_token}"
        }
        res = Requests_Utils().send_Requests('get', url=url, data=params)
        # res = requests.get(url,params=params)
        # res = requests.request('get',url,params=params)
        # print(res.json(),type(res.json()))                #打印返回的数据，格式：字典格式
        # print(res.content,type(res.content))              #打印返回的数据，格式：字节类型


    def test_edit_flag(self):
        '''
        编辑标签接口
        :return:
        '''
        url = r"/cgi-bin/tags/update?access_token=" + "${access_token}" + ""
        json_data = {"tag":{"id":127,"name":"SS" + str(int(time.time()))}}
        # print(json_data,type(json_data))
        # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        # data = json.dumps(json_data)
        # data_new = {"tag": {"id": 127, "name": "SS2121952988"}}
        # print(data_new,type(data_new))
        # res = requests.post(url,json=json_data)
        # res = requests.request('post',url,json=json_data)
        res = Requests_Utils().send_Requests('post', url=url, data=json_data)
        # print(res.json(),type(res.json()))


    def test_file_upload(self):
        '''

        :return:
        '''
        url = r"/cgi-bin/media/uploadimg?access_token=" + "${access_token}" + ""
        file_data = \
            {"media" : open( "D:\WALL_PAPERS\wallhaven-vgj7pl.png",'rb')}
        # res = requests.post(url,files=file_data)
        res = Requests_Utils().send_Requests('post', url=url, files=file_data)
        # res = requests.request('post',url,files=file_data)
        print(res.json(),type(res.json()))



    # def test_goto_index(self):
    #     '''
    #     访问网站 phpwind
    #     :return:
    #     '''
    #     url = r"http://47.107.116.139/phpwind/"
    #     parames = {}
    #     # res = requests.get(url,params=parames)
    #     res = requests.request('get',url,params=parames)
    #     print(res.text)
    #     #正则表达式取值,并赋值给类的变量（全局变量）
    #     obj = re.search('name="csrf_token" value="(.+?)"',res.text)
    #     Requests_Sends.csrf_token = obj.group(1)
    #     #获取到页面上返回的cookie数据，并复制给类的变量（全局变量）
    #     Requests_Sends.phpwind_cookie = res.cookies



    # def test_login_phpwind(self):
    #     '''
    #     登录接口
    #     :return:
    #     '''
    #     url = r"http://47.107.116.139/phpwind/index.php?m=u&c=login&a=dorun"
    #     req_header = {
    #         "Accept": "application/json, text/javascript, /; q=0.01",
    #         "X-Requested-With": "XMLHttpRequest"
    #     }
    #     req_cookie = Requests_Sends.phpwind_cookie
    #     datas = {
    #         "username": "admin",
    #         "password": "msxy",
    #         "csrf_token": Requests_Sends.csrf_token,
    #         "backurl": "http://47.107.116.139/phpwind/",
    #         "invite": ""
    #     }
    #     print("datas的格式为：",type(datas))
    #     # res =  requests.post(url,data=datas,headers=req_header,cookies=req_cookie)
    #     res = requests.request('post',url,data=datas,headers=req_header,cookies=req_cookie)
    #     print(res.json())




if __name__ == '__main__':
    Requests_Sends().get_token()
    Requests_Sends().edit_flag()
    Requests_Sends().get_flag()
    Requests_Sends().file_upload()
    # Requests_Sends().goto_index()
    # Requests_Sends().login_phpwind()
