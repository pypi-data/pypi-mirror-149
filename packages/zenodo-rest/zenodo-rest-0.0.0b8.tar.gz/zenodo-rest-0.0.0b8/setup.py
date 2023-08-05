import io
import os
import re

from setuptools import find_packages, setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type("")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


setup(
    name="zenodo-rest",
    version="0.0.0b8",
    py_modules=["zenodo_rest"],
    url="https://github.com/kykrueger/zenodo-rest-python.git",
    license="MIT",
    author="Kyle Krueger",
    author_email="kyle.s.krueger@gmail.com",
    description=(
        "A python wrapper of Zenodo's REST API",
        "for python and the command line.",
    ),
    long_description=read("README.md"),
    packages=find_packages(exclude=("tests",)),
    install_requires=["click", "pydantic", "python-dotenv", "requests"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "zenodo-rest = zenodo_rest.cli:cli",
        ],
    },
)
