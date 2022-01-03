import re
from setuptools import setup

INSTALL_REQUIRES = ["sphinx"]
EXTRAS_REQUIRE = {
    "tests": ["pytest"],
    "lint": [
        "flake8==3.9.2",
        "flake8-bugbear==20.11.1",
        "pre-commit~=2.7",
    ],
}
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["lint"] + ["tox"]


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ""
    with open(fname) as fp:
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
    description="A Sphinx extension for linking to your project's issue tracker",
    long_description=read("README.rst"),
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    author="Steven Loria",
    author_email="sloria1@gmail.com",
    url="https://github.com/sloria/sphinx-issues",
    license="MIT",
    keywords="sphinx issues github",
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Documentation",
    ],
    py_modules=["sphinx_issues"],
    project_urls={"Issues": "https://github.com/sloria/sphinx-issues/issues"},
)
