# -*- coding: utf-8 -*-
"""A Sphinx extension for linking to your project's issue tracker."""
from docutils import nodes, utils
from sphinx.util.nodes import split_explicit_title

__version__ = "1.1.0"
__author__ = "Steven Loria"
__license__ = "MIT"


def user_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """Sphinx role for linking to a user profile. Defaults to linking to
    Github profiles, but the profile URIS can be configured via the
    ``issues_user_uri`` config value.

    Examples: ::

        :user:`sloria`

    Anchor text also works: ::

        :user:`Steven Loria <sloria>`
    """
    options = options or {}
    content = content or []
    has_explicit_title, title, target = split_explicit_title(text)

    target = utils.unescape(target).strip()
    title = utils.unescape(title).strip()
    config = inliner.document.settings.env.app.config
    if config.issues_user_uri:
        ref = config.issues_user_uri.format(user=target)
    else:
        ref = "https://github.com/{0}".format(target)
    if has_explicit_title:
        text = title
    else:
        text = "@{0}".format(target)

    link = nodes.reference(text=text, refuri=ref, **options)
    return [link], []


def cve_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """Sphinx role for linking to a CVE on https://cve.mitre.org.

    Examples: ::

        :cve:`CVE-2018-17175`

    """
    options = options or {}
    content = content or []
    has_explicit_title, title, target = split_explicit_title(text)

    target = utils.unescape(target).strip()
    title = utils.unescape(title).strip()
    ref = "https://cve.mitre.org/cgi-bin/cvename.cgi?name={0}".format(target)
    text = title if has_explicit_title else target
    link = nodes.reference(text=text, refuri=ref, **options)
    return [link], []


class IssueRole(object):
    def __init__(self, uri_config_option, format_kwarg, github_uri_template):
        self.uri_config_option = uri_config_option
        self.format_kwarg = format_kwarg
        self.github_uri_template = github_uri_template

    def make_node(self, issue_no, config, options=None):
        options = options or {}
        if issue_no not in ("-", "0"):
            uri_template = getattr(config, self.uri_config_option, None)
            if uri_template:
                ref = uri_template.format(**{self.format_kwarg: issue_no})
            elif config.issues_github_path:
                ref = self.github_uri_template.format(
                    issues_github_path=config.issues_github_path, n=issue_no
                )
            else:
                raise ValueError(
                    "Neither {} nor issues_github_path "
                    "is set".format(self.uri_config_option)
                )
            issue_text = "#{0}".format(issue_no)
            link = nodes.reference(text=issue_text, refuri=ref, **options)
        else:
            link = None
        return link

    def __call__(
        self, name, rawtext, text, lineno, inliner, options=None, content=None
    ):
        options = options or {}
        content = content or []
        issue_nos = [each.strip() for each in utils.unescape(text).split(",")]
        config = inliner.document.settings.env.app.config
        ret = []
        for i, issue_no in enumerate(issue_nos):
            node = self.make_node(issue_no, config, options=options)
            ret.append(node)
            if i != len(issue_nos) - 1:
                sep = nodes.raw(text=", ", format="html")
                ret.append(sep)
        return ret, []


"""Sphinx role for linking to an issue. Must have
`issues_uri` or `issues_github_path` configured in ``conf.py``.
Examples: ::
    :issue:`123`
    :issue:`42,45`
"""
issue_role = IssueRole(
    uri_config_option="issues_uri",
    format_kwarg="issue",
    github_uri_template="https://github.com/{issues_github_path}/issues/{n}",
)

"""Sphinx role for linking to a pull request. Must have
`issues_pr_uri` or `issues_github_path` configured in ``conf.py``.
Examples: ::
    :pr:`123`
    :pr:`42,45`
"""
pr_role = IssueRole(
    uri_config_option="issues_pr_uri",
    format_kwarg="pr",
    github_uri_template="https://github.com/{issues_github_path}/pull/{n}",
)


def setup(app):
    # Format template for issues URI
    # e.g. 'https://github.com/sloria/marshmallow/issues/{issue}
    app.add_config_value("issues_uri", default=None, rebuild="html")
    # Format template for PR URI
    # e.g. 'https://github.com/sloria/marshmallow/pull/{issue}
    app.add_config_value("issues_pr_uri", default=None, rebuild="html")
    # Shortcut for Github, e.g. 'sloria/marshmallow'
    app.add_config_value("issues_github_path", default=None, rebuild="html")
    # Format template for user profile URI
    # e.g. 'https://github.com/{user}'
    app.add_config_value("issues_user_uri", default=None, rebuild="html")
    app.add_role("issue", issue_role)
    app.add_role("pr", pr_role)
    app.add_role("user", user_role)
    app.add_role("cve", cve_role)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
