# _*_ coding:utf-8 _*_
# ------------------------
# @Author   :    Jack    -
# @Time     : 2022-04-14 -
#   Time never speaks,   -
# but proves many things -
# ------------------------

"""长描述long_description，一般写在readme.md中，读出来之后赋值给对应字段

这里是做一个简单的测试，在规范上可能没有太苛刻的要求
"""


import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="jin_test_packet",  # 包的分发名称
    version="0.0.1",    # 包版本
    description="这是我的第一个资源包，仅仅是测试如何制作资源包并上传PYPI",  # 包的简短描述
    author="Jack_jin",   # 作者
    long_description=long_description,   # 长描述，对这个包的功能的具体描述，一般写在readme.md中
    author_email="2960688709@qq.com",   # 作者邮箱
    url="",  # 项目主页的url，就是git仓库的地址
    packages=setuptools.find_packages(),  # 我们所依赖的其他包，这里使用find_packages()自动发现，无需手动列出
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]  # 告诉索引并点一些关于你的包的其他元数据。具体可以参考 https://pypi.org/classifiers/
)
