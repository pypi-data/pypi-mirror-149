# -*- coding: UTF-8 -*-
import setuptools


with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
  name="luckylog",
  version="1.0.4",
  author="测码课堂-范晔",
  author_email="1538379200@qq.com",
  description="自定义日志模式",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)