#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: zhaojunhang
# Mail: 454706391@qq.com
# Created Time:  2022-05-07
#############################################


from setuptools import setup, find_packages

setup(
    name = "fsbot",
    version = "0.1.2",
    keywords = ("feishu"),
    description = "fei shu notification",
    long_description = "fei shu notification",
    license = "MIT Licence",

    url = "https://github.com/zhaojunhang/feishu_notification.git",
    author = "zhaojunhang",
    author_email = "454706391@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['requests','logging','urllib3']
)
