#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   logger_utils.py    
@Contact :   sasewhite@live.com
@License :   (C)Copyright 2017-2021, 114S-342t-3Y

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/2 10:31   Mige      1.0         None
'''
import datetime
import logging

from common.common_utils import get_object_path, read_config_yaml


class Logger_Utils:

    def create_Log(self):
        # 创建一个logger对象
        self.logger = logging.getLogger('log')
        if not self.logger.handlers:
            # 设置全局日志级别
            self.logger.setLevel(logging.DEBUG)
            # 设置日志文件的路径
            self.file_path = get_object_path() + "logs/" + read_config_yaml('log',
                                                                            'log_name') + datetime.datetime.now().strftime(
                '%Y-%m-%d-%H-%M') + '.log'
            # print(self.file_path)
            # 创建日志文件的处理器 handler
            self.file_handler = logging.FileHandler(self.file_path, encoding='utf-8')
            # 单独设置文件日志的级别 从config.yml文件中取  log_level
            file_log_level = str(read_config_yaml('log', 'log_level')).lower()
            if file_log_level == 'deebug':
                self.file_handler.setLevel(logging.DEBUG)
            elif file_log_level == 'info':
                self.file_handler.setLevel(logging.INFO)
            elif file_log_level == 'warning':
                self.file_handler.setLevel(logging.WARNING)
            elif file_log_level == 'error':
                self.file_handler.setLevel(logging.ERROR)
            elif file_log_level == 'critical':
                self.file_handler.setLevel(logging.CRITICAL)
            # 设置日志文件的格式
            self.file_handler.setFormatter(logging.Formatter(read_config_yaml('log', 'log_format')))
            # 将文件处理器加入到日志器上
            self.logger.addHandler(self.file_handler)
            # 控制台处理器
            self.console_handler = logging.StreamHandler()
            self.console_handler.setLevel(logging.DEBUG)
            self.console_handler.setFormatter(logging.Formatter(read_config_yaml('log', 'log_format')))
            self.logger.addHandler(self.console_handler)
        return self.logger

def write_log(log_message):
    Logger_Utils().create_Log().info(log_message)
    
def error_log(log_message):
    Logger_Utils().create_Log().info(log_message)
    raise Exception(log_message)
