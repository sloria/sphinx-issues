# -*- coding: utf-8 -*-
import sys
import webbrowser

from invoke import task


@task
def test(ctx, syntax=True, watch=False, last_failing=False):
    """Run the tests.

    Note: --watch requires pytest-xdist to be installed.
    """
    import pytest

    if syntax:
        flake(ctx)
    args = []
    if watch:
        args.append("-f")
    if last_failing:
        args.append("--lf")
    retcode = pytest.main(args)
    sys.exit(retcode)


@task
def flake(ctx):
    """Run flake8 on codebase."""
    ctx.run("flake8 .", echo=True)


@task
def readme(ctx, browse=False):
    ctx.run("rst2html.py README.rst > README.html")
    if browse:
        webbrowser.open_new_tab("README.html")


@task
def clean(ctx):
    ctx.run("rm -rf build")
    ctx.run("rm -rf dist")
    ctx.run("rm -rf sphinx-issues.egg-info")
    print("Cleaned up.")
