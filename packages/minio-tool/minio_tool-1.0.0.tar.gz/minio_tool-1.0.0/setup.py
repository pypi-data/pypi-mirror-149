# -*- coding: utf-8 -*-
"""
@CreateTime     2022-05-06 18:33
@Author         sosdawn
@File           setup.py
@Software       PyCharm
@Project        minio_tool
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='minio_tool',
    version='1.0.0',
    description='minio 创建/删除 bucket, 上传文件等',
    author='ikxyang',
    author_email='sosdawn@163.com',
    install_requires=required,
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitee.com/ikxyang/minio_tool.git',
    # 如果有的文件不用打包，则只能指定需要打包的文件
    # packages=['代码1','代码2','__init__']  #指定目录中需要打包的py文件，注意不要.py后缀
    license="apache 3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# python3 -m pip install --user --upgrade setuptools wheel  # 确保拥有setuptools并wheel 安装了最新版本
# python3 setup.py sdist bdist_wheel
#
# python3 -m pip install --user --upgrade twine  # 安装twine
# twine upload dist/*
