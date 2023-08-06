#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="filebox",
    version="0.0.12",
    author="ZeroSeeker",
    author_email="zeroseeker@foxmail.com",
    description="make it easy to manage file",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/ZeroSeeker/filebox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests==2.27.1',
        'showlog==0.0.6',
        'urllib3==1.26.9',
        'xlrd==2.0.1',
        'openpyxl==3.0.9',
        'dictbox==0.0.2'
    ]
)
