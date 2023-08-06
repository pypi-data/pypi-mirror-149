# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

file = open("README.md", "r",encoding="utf-8")
readme = file.read()
file.close()

setup(
    name="lzlib",
    version="1.0.0",
    description="这是lzlib",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="LiuZhen",
    author_email="15936066606@163.com",
    url="https://github.com/liuzhen6606/lzlib",
    packages=find_packages(),
    package_dir={"": "src"},
    install_requires=["linhhh"],
    extras_require={},
    include_package_data=True,
    license='MIT',
    project_urls={"Home": "https://github.com/liuzhen6606/lzlib"},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
