# -*- coding: utf-8 -*-
from invoke import task, run


@task
def readme(browse=False):
    run('rst2html.py README.rst > README.html')


@task
def publish(test=False):
    """Publish to the cheeseshop."""
    if test:
        run('python setup.py register -r test sdist upload -r test')
    else:
        run("python setup.py register sdist upload")
