#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   conftest.py    
@Contact :   sasewhite@live.com
@License :   (C)Copyright 2017-2021, 114S-342t-3Y

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/5/28 11:26   Mige      1.0         None
'''
import pytest

from common.common_utils import clear_extract_yaml


@pytest.fixture(scope='session', autouse=True)
def clear_extract():
    print()
    print("----------------------开始执行fixture-clear_extract_yaml方法-------------------------------------")
    clear_extract_yaml()
