# encoding: utf-8
"""
@author: yanghao
@contact: yanghao170@aliyun.com
@time: 2022/5/5 16:43
@file: setup.py
@desc: 
"""
import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="autumn_rain_py_sdk",  # Replace with your own username
    version="0.0.1",
    author="qiwa",
    author_email="yanghao170@aliyun.com",
    description="python相关的通用工具集合",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/yanghao170/autumn_rain_py_sdk.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
