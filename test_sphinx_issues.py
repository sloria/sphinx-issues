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
    setup as issues_setup
)

import pytest

@pytest.yield_fixture(params=[
    # Parametrize config
    {'issues_github_path': 'sloria/marshmallow'},
    {'issues_uri': 'https://github.com/sloria/marshmallow/issues/{issue}'}
])
def app(request):
    src, doctree, confdir, outdir = [mkdtemp() for _ in range(4)]
    Sphinx._log = lambda self, message, wfile, nonl=False: None
    app = Sphinx(
        srcdir=src,
        confdir=None,
        outdir=outdir,
        doctreedir=doctree,
        buildername='html',
    )
    issues_setup(app)
    # Stitch together as the sphinx app init() usually does w/ real conf files
    app.config._raw_config = request.param
    app.config.init_values(warn=False)
    yield app
    [rmtree(x) for x in (src, doctree, confdir, outdir)]

@pytest.fixture()
def inliner(app):
    return Mock(document=Mock(settings=Mock(env=Mock(app=app))))

def test_issue_role(inliner):
    result = issue_role(
        name=None,
        rawtext='',
        text='42',
        lineno=None,
        inliner=inliner
    )
    link = result[0][0]
    assert link.astext() == '#42'
    assert link.attributes['refuri'] == 'https://github.com/sloria/marshmallow/issues/42'

def test_issue_role_multiple(inliner):
    result = issue_role(
        name=None,
        rawtext='',
        text='42,43',
        inliner=inliner,
        lineno=None,
    )
    link1 = result[0][0]
    assert link1.astext() == '#42'
    assert link1.attributes['refuri'] == 'https://github.com/sloria/marshmallow/issues/42'

    sep = result[0][1]
    assert sep.astext() == ', '

    link2 = result[0][2]
    assert link2.astext() == '#43'
    assert link2.attributes['refuri'] == 'https://github.com/sloria/marshmallow/issues/43'
