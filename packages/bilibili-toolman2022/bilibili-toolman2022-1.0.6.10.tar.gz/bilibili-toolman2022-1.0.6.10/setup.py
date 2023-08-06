# -*- coding: utf-8 -*-
import setuptools,bilibili_toolman

requirements = [
    requirement.strip() for requirement in open('requirements.txt','r').readlines()
]

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="bilibili-toolman2022",
    version=bilibili_toolman.__version__,
    author="greats3an",
    author_email="greats3an@gmail.com",
    description=bilibili_toolman.__desc__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/redy112/bilibilitoolman2022",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],install_requires=requirements,
    python_requires='>=3.6',
)
