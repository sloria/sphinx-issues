# -*- coding: utf-8 -*-
import re
from setuptools import setup


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version('sphinx_issues.py')


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name='sphinx-issues',
    version=__version__,
    description="A Sphinx extension for linking to your project's "
                "issue tracker",
    long_description=read('README.rst'),
    install_requires=['sphinx'],
    author='Steven Loria',
    author_email='sloria1@gmail.com',
    url='https://github.com/sloria/sphinx-issues',
    license=read('LICENSE'),
    keywords='sphinx,issues,github',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Documentation',
    ],
    py_modules=['sphinx_issues']
)
