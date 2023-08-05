from setuptools import setup, find_packages
import sys
import os

setup(
    name="nonebot_plugin_bilibilibot",
    version="2.0.4",
    author="TDK",
    author_email="tdk1969@foxmail.com",
    description="基于Nonebot的bilibili通知插件，可将up主，主播以及番剧的更新/直播动态推送到QQ",
    long_description=open("README.rst", "r").read(),
    include_package_data=True,
    license="GNU",
    url="https://github.com/TDK1969/nonebot_plugin_bilibilibot",
    packages=['nonebot_plugin_bilibilibot'],
    install_requires=[
        "requests",
        "nonebot_plugin_apscheduler",
        "nonebot_adapter_onebot"
    ],
    keywords='nonebot',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],

)