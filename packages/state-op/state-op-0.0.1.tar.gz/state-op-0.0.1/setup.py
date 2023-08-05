#! -*- coding: utf-8 -*-

import pathlib
from setuptools import setup
from setuptools import find_packages

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="state-op",
    version="0.0.1",
    description="A state engine for natural language processing that supports custom operators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/DengBoCong/state-op",
    author="DengBoCong",
    author_email="bocongdeng@gmail.com",
    install_requires=[],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="state, nlp",
    project_urls={
        "Bug Reports": "https://github.com/DengBoCong/state-op/issues",
        "Funding": "https://github.com/DengBoCong/state-op",
        "Source": "https://github.com/DengBoCong/state-op",
    },
)
