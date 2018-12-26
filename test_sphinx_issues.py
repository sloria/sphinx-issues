# -*- coding: utf-8 -*-
from tempfile import mkdtemp
from shutil import rmtree

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from sphinx.application import Sphinx
from sphinx_issues import (
    issue_role,
    user_role,
    pr_role,
    cve_role,
    commit_role,
    setup as issues_setup,
)

import pytest


@pytest.yield_fixture(
    params=[
        # Parametrize config
        {"issues_github_path": "marshmallow-code/marshmallow"},
        {
            "issues_uri": "https://github.com/marshmallow-code/marshmallow/issues/{issue}",
            "issues_pr_uri": "https://github.com/marshmallow-code/marshmallow/pull/{pr}",
            "issues_commit_uri": "https://github.com/marshmallow-code/marshmallow/commit/{commit}",
        },
    ]
)
def app(request):
    src, doctree, confdir, outdir = [mkdtemp() for _ in range(4)]
    Sphinx._log = lambda self, message, wfile, nonl=False: None
    app = Sphinx(
        srcdir=src, confdir=None, outdir=outdir, doctreedir=doctree, buildername="html"
    )
    issues_setup(app)
    # Stitch together as the sphinx app init() usually does w/ real conf files
    app.config._raw_config = request.param
    try:
        app.config.init_values()
    except TypeError:
        app.config.init_values(lambda x: x)
    yield app
    [rmtree(x) for x in (src, doctree, confdir, outdir)]


@pytest.fixture()
def inliner(app):
    return Mock(document=Mock(settings=Mock(env=Mock(app=app))))


def test_issue_role(inliner):
    result = issue_role(name=None, rawtext="", text="42", lineno=None, inliner=inliner)
    link = result[0][0]
    assert link.astext() == "#42"
    issue_url = "https://github.com/marshmallow-code/marshmallow/issues/42"
    assert link.attributes["refuri"] == issue_url


def test_issue_role_multiple(inliner):
    result = issue_role(
        name=None, rawtext="", text="42,43", inliner=inliner, lineno=None
    )
    link1 = result[0][0]
    assert link1.astext() == "#42"
    issue_url = "https://github.com/marshmallow-code/marshmallow/issues/"
    assert link1.attributes["refuri"] == issue_url + "42"

    sep = result[0][1]
    assert sep.astext() == ", "

    link2 = result[0][2]
    assert link2.astext() == "#43"
    assert link2.attributes["refuri"] == issue_url + "43"


def test_user_role(inliner):
    result = user_role("user", rawtext="", text="sloria", inliner=inliner, lineno=None)
    link = result[0][0]
    assert link.astext() == "@sloria"
    assert link.attributes["refuri"] == "https://github.com/sloria"


def test_user_role_explicit_name(inliner):
    result = user_role(
        "user", rawtext="", text="Steven Loria <sloria>", inliner=inliner, lineno=None
    )
    link = result[0][0]
    assert link.astext() == "Steven Loria"
    assert link.attributes["refuri"] == "https://github.com/sloria"


def test_pr_role(inliner):
    result = pr_role(name=None, rawtext="", text="42", lineno=None, inliner=inliner)
    link = result[0][0]
    assert link.astext() == "#42"
    issue_url = "https://github.com/marshmallow-code/marshmallow/pull/42"
    assert link.attributes["refuri"] == issue_url


def test_cve_role(inliner):
    result = cve_role(
        name=None, rawtext="", text="CVE-2018-17175", lineno=None, inliner=inliner
    )
    link = result[0][0]
    assert link.astext() == "CVE-2018-17175"
    issue_url = "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-17175"
    assert link.attributes["refuri"] == issue_url


def test_commit_role(inliner):
    sha = "123abc456def"
    result = commit_role(name=None, rawtext="", text=sha, lineno=None, inliner=inliner)
    link = result[0][0]
    assert link.astext() == sha[:7]
    url = "https://github.com/marshmallow-code/marshmallow/commit/{}".format(sha)
    assert link.attributes["refuri"] == url
