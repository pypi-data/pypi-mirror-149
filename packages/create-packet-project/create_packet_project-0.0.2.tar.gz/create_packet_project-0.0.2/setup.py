"""资源包配置文件

name：对应的字段是资源包的名称，尽量简短突出重点
version：对应的是版本号，不能写的太大，第一版建议从0.0.1或0.1开始
description：是对资源包的描述，尽量简短
author: 作者名称
long_description：长描述，这一部分是从README.md文件中读取到的，主要是对资源包用法的介绍
author_email: 作者邮箱，一般是被人给你提问题用，自己用的话可有可无
url： 项目仓库地址
packages：我们所依赖的其他包，这里使用find_packages()自动发现，无需手动列出
classifiers: 现在理解不是很深，不做过多解释，具体可以参考 https://pypi.org/classifiers/
"""
import setuptools

# 读资源包的详细描述信息，其中包括资源包的详细用法
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="create_packet_project",
    version="0.0.2",
    description="自动生成创建资源包所需要的文件",
    author="jack_jin",
    long_description=long_description,
    author_email="2960688709@qq.com",
    url="https://gitee.com/jin-yongqing/create_packet.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

