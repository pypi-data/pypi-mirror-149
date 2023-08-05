# -*- coding: utf-8 -*-
# Author: Jimei Shen
from setuptools import find_packages, setup

requires_list = open(f'EyeCatching/requirements.txt', 'r', encoding='utf8').readlines()
requires_list = [i.strip() for i in requires_list]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='eyecatching',
    version='0.0.5',
    author="Jimei",
    author_email='shenjimei33@outlook.com',
    description="eye catching",
    python_requires="==3.7.*",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"EyeCatching/haarcascades": ["*"],
                  "EyeCatching/templates":["*"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=requires_list,
    url="https://github.com/ShenJimei",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",

    ],
    entry_points={
        "console_scripts": [
            "realpython=eyecatching.main:main",
        ]}
)