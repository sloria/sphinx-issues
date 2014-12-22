# -*- coding: utf-8 -*-
import sys

from invoke import task, run

@task
def test():
    """Run the tests."""
    run('py.test', echo=True, pty=True)

@task
def readme(browse=False):
    run('rst2html.py README.rst > README.html')


@task
def publish(test=False):
    """Publish to the cheeseshop."""
    try:
        __import__('wheel')
    except ImportError:
        print("wheel required. Run `pip install wheel`.")
        sys.exit(1)
    if test:
        run('python setup.py register -r test sdist bdist_wheel upload -r test')
    else:
        run("python setup.py register sdist bdist_wheel upload")
