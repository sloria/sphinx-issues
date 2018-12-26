# -*- coding: utf-8 -*-
import re
from setuptools import setup

INSTALL_REQUIRES = ["sphinx"]
EXTRAS_REQUIRE = {
    "tests": ["pytest", 'mock; python_version < "3.0"'],
    "lint": [
        "flake8==3.6.0",
        'flake8-bugbear==18.8.0; python_version >= "3.5"',
        "pre-commit==1.13.0",
    ],
}
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["lint"] + ["tox"]


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ""
    with open(fname, "r") as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError("Cannot find version information")
    return version


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name="sphinx-issues",
    version=find_version("sphinx_issues.py"),
    description="A Sphinx extension for linking to your project's " "issue tracker",
    long_description=read("README.rst"),
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    author="Steven Loria",
    author_email="sloria1@gmail.com",
    url="https://github.com/sloria/sphinx-issues",
    license="MIT",
    keywords="sphinx issues github",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Documentation",
    ],
    py_modules=["sphinx_issues"],
    project_urls={"Issues": "https://github.com/sloria/sphinx-issues/issues"},
)
