import subprocess
import sys
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from unittest.mock import Mock

import pytest
import sphinx.application

from sphinx_issues import (
    commit_role,
    issue_role,
    pr_role,
    pypi_role,
    user_role,
)
from sphinx_issues import setup as issues_setup

BASE_DIR = Path(__file__).parent.absolute()


@pytest.fixture(
    params=[
        # Parametrize config
        {"issues_github_path": "marshmallow-code/marshmallow"},
        {"issues_default_group_project": "marshmallow-code/marshmallow"},
        {
            "issues_uri": "https://github.com/marshmallow-code/marshmallow/issues/{issue}",
            "issues_pr_uri": "https://github.com/marshmallow-code/marshmallow/pull/{pr}",
            "issues_commit_uri": "https://github.com/marshmallow-code/marshmallow/commit/{commit}",
        },
    ]
)
def app(request):
    src, doctree, confdir, outdir = (mkdtemp() for _ in range(4))
    sphinx.application.Sphinx._log = lambda self, message, wfile, nonl=False: None
    app = sphinx.application.Sphinx(
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


@pytest.mark.parametrize(
    ("role", "role_name", "text", "expected_text", "expected_url"),
    [
        (
            issue_role,
            "issue",
            "42",
            "#42",
            "https://github.com/marshmallow-code/marshmallow/issues/42",
        ),
        (
            issue_role,
            "issue",
            "Hard Issue <42>",
            "Hard Issue",
            "https://github.com/marshmallow-code/marshmallow/issues/42",
        ),
        (
            issue_role,
            "issue",
            "Not my business <foo/bar#42>",
            "Not my business",
            "https://github.com/foo/bar/issues/42",
        ),
        (
            pr_role,
            "pr",
            "42",
            "#42",
            "https://github.com/marshmallow-code/marshmallow/pull/42",
        ),
        (user_role, "user", "sloria", "@sloria", "https://github.com/sponsors/sloria"),
        (
            user_role,
            "user",
            "Steven Loria <sloria>",
            "Steven Loria",
            "https://github.com/sponsors/sloria",
        ),
        (
            pypi_role,
            "pypi",
            "sphinx-issues",
            "sphinx-issues",
            "https://pypi.org/project/sphinx-issues",
        ),
        (
            commit_role,
            "commit",
            "123abc456def",
            "@123abc4",
            "https://github.com/marshmallow-code/marshmallow/commit/123abc456def",
        ),
        # External issue
        (
            issue_role,
            "issue",
            "sloria/webargs#42",
            "sloria/webargs#42",
            "https://github.com/sloria/webargs/issues/42",
        ),
        # External PR
        (
            pr_role,
            "pr",
            "sloria/webargs#42",
            "sloria/webargs#42",
            "https://github.com/sloria/webargs/pull/42",
        ),
        # External commit
        (
            commit_role,
            "commit",
            "sloria/webargs@abc123def456",
            "sloria/webargs@abc123d",
            "https://github.com/sloria/webargs/commit/abc123def456",
        ),
    ],
)
def test_roles(inliner, role, role_name, text, expected_text, expected_url):
    result = role(role_name, rawtext="", text=text, lineno=None, inliner=inliner)
    link = result[0][0]
    assert link.astext() == expected_text
    assert link.attributes["refuri"] == expected_url


def test_issue_role_multiple(inliner):
    result = issue_role(
        name=None, rawtext="", text="a title <42>,43", inliner=inliner, lineno=None
    )
    link1 = result[0][0]
    assert link1.astext() == "a title"
    issue_url = "https://github.com/marshmallow-code/marshmallow/issues/"
    assert link1.attributes["refuri"] == issue_url + "42"

    sep = result[0][1]
    assert sep.astext() == ", "

    link2 = result[0][2]
    assert link2.astext() == "#43"
    assert link2.attributes["refuri"] == issue_url + "43"


def test_issue_role_multiple_with_external(inliner):
    result = issue_role(
        "issue", rawtext="", text="42,sloria/konch#43", inliner=inliner, lineno=None
    )
    link1 = result[0][0]
    assert link1.astext() == "#42"
    issue_url = "https://github.com/marshmallow-code/marshmallow/issues/42"
    assert link1.attributes["refuri"] == issue_url

    sep = result[0][1]
    assert sep.astext() == ", "

    link2 = result[0][2]
    assert link2.astext() == "sloria/konch#43"
    assert link2.attributes["refuri"] == "https://github.com/sloria/konch/issues/43"


@pytest.fixture
def app_custom_uri():
    src, doctree, confdir, outdir = (mkdtemp() for _ in range(4))
    sphinx.application.Sphinx._log = lambda self, message, wfile, nonl=False: None
    app = sphinx.application.Sphinx(
        srcdir=src, confdir=None, outdir=outdir, doctreedir=doctree, buildername="html"
    )
    issues_setup(app)
    # Stitch together as the sphinx app init() usually does w/ real conf files
    app.config._raw_config = {
        "issues_default_group_project": "myteam/super_great_project",
        "issues_uri": "https://gitlab.company.com/{group}/{project}/-/issues/{issue}",
        "issues_prefix": "#",
        "issues_pr_uri": "https://gitlab.company.com/{group}/{project}/-/merge_requests/{pr}",
        "issues_pr_prefix": "!",
        "issues_commit_uri": "https://gitlab.company.com/{group}/{project}/-/commit/{commit}",
        "issues_commit_prefix": "@",
        "issues_user_uri": "https://gitlab.company.com/{user}",
        "issues_user_prefix": "@",
    }
    try:
        app.config.init_values()
    except TypeError:
        app.config.init_values(lambda x: x)
    yield app
    [rmtree(x) for x in (src, doctree, confdir, outdir)]


@pytest.fixture()
def inliner_custom_uri(app_custom_uri):
    return Mock(document=Mock(settings=Mock(env=Mock(app=app_custom_uri))))


@pytest.mark.parametrize(
    ("role", "role_name", "text", "expected_text", "expected_url"),
    [
        (
            issue_role,
            "issue",
            "42",
            "#42",
            "https://gitlab.company.com/myteam/super_great_project/-/issues/42",
        ),
        (
            issue_role,
            "issue",
            "Hard Issue <42>",
            "Hard Issue",
            "https://gitlab.company.com/myteam/super_great_project/-/issues/42",
        ),
        (
            issue_role,
            "issue",
            "Not my business <foo/bar#42>",
            "Not my business",
            "https://gitlab.company.com/foo/bar/-/issues/42",
        ),
        (
            pr_role,
            "pr",
            "42",
            "!42",
            "https://gitlab.company.com/myteam/super_great_project/-/merge_requests/42",
        ),
        (user_role, "user", "sloria", "@sloria", "https://gitlab.company.com/sloria"),
        (
            user_role,
            "user",
            "Steven Loria <sloria>",
            "Steven Loria",
            "https://gitlab.company.com/sloria",
        ),
        (
            commit_role,
            "commit",
            "123abc456def",
            "@123abc4",
            "https://gitlab.company.com/myteam/super_great_project/-/commit/123abc456def",
        ),
        # External issue
        (
            issue_role,
            "issue",
            "sloria/webargs#42",
            "sloria/webargs#42",
            "https://gitlab.company.com/sloria/webargs/-/issues/42",
        ),
        # External PR
        (
            pr_role,
            "pr",
            "sloria/webargs#42",
            "sloria/webargs!42",
            "https://gitlab.company.com/sloria/webargs/-/merge_requests/42",
        ),
        # External commit
        (
            commit_role,
            "commit",
            "sloria/webargs@abc123def456",
            "sloria/webargs@abc123d",
            "https://gitlab.company.com/sloria/webargs/-/commit/abc123def456",
        ),
    ],
)
def test_roles_custom_uri(
    inliner_custom_uri, role, role_name, text, expected_text, expected_url
):
    result = role(
        role_name, rawtext="", text=text, lineno=None, inliner=inliner_custom_uri
    )
    link = result[0][0]
    assert link.astext() == expected_text
    assert link.attributes["refuri"] == expected_url


@pytest.fixture
def tmp_doc_build_folder(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Generate a temporary source folder and chdir in it. Return the build folder"""
    source = tmp_path / "source"
    build = tmp_path / "build"
    static = source / "_static"
    for folder in (source, build, static):
        folder.mkdir()
    conf_py = BASE_DIR / "source" / "conf.py"
    examples_rst = BASE_DIR / "source" / "examples.rst"

    source.joinpath("conf.py").write_bytes(conf_py.read_bytes())
    source.joinpath("index.rst").write_bytes(examples_rst.read_bytes())

    monkeypatch.chdir(source)
    return build


def test_sphinx_build_integration(tmp_doc_build_folder: Path):
    """Ensure that a simulated complete sphinx run works as expected"""
    subprocess.run(
        [
            Path(sys.executable).parent.joinpath("sphinx-build"),
            "-b",
            "html",
            "-W",  # turn warnings into errors
            "-E",  # force rebuild of environment (even if we work in tmp)
            ".",
            str(tmp_doc_build_folder),
        ],
        check=True,
    )

    created = tmp_doc_build_folder / "index.html"
    assert created.exists() and created.is_file()
    content = created.read_text()
    issue_url = "https://gitlab.company.com/myteam/super_great_project/-/issues/"
    other_issue_url = "https://gitlab.company.com/sloria/konch/-/issues/"
    pr_url = "https://gitlab.company.com/myteam/super_great_project/-/merge_requests/"
    user_url = "https://gitlab.company.com/"

    # We could do something fancy like an HTML parser or regex:
    # Instead we keep it simple
    expected_strings = (
        (
            f"See issues "
            f'<a class="reference external" href="{issue_url}12">#12</a>, '
            f'<a class="reference external" href="{issue_url}13">#13</a>'
        ),
        (
            f"See other issues "
            f'<a class="reference external" href="{other_issue_url}45">sloria/konch#45</a>,'
            f' <a class="reference external" href="{issue_url}46">#46</a>'
        ),
        (
            f'See PR <a class="reference external" href="{pr_url}58">!58</a>, '
            f'thanks <a class="reference external" href="{user_url}kound">&#64;kound</a>'
        ),
    )
    # Ensure that we do no check character wise but line wise
    assert len(expected_strings) == 3

    for expected in expected_strings:
        assert expected in content
