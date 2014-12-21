# -*- coding: utf-8 -*-
"""A Sphinx extension for linking to your project's issue tracker."""
from docutils import nodes, utils

__version__ = '0.1.0'

def make_node(issue_no, config, options=None):
    if issue_no not in ('-', '0'):
        if config.issues_uri:
            ref = config.issues_uri.format(issue=issue_no)
        elif config.issues_github_path:
            ref = 'https://github.com/{0}/issues/{1}'.format(
                config.issues_github_path, issue_no
            )
        issue_text = '#{0}'.format(issue_no)
        link = nodes.reference(text=issue_text, refuri=ref, **options)
    else:
        link = None
    return link


def issue_role(name, rawtext, text, lineno,
               inliner, options=None, content=None):
    """Sphinx role for linking to an issue. Must have
    `issues_uri` or `issues_github_path` configured in ``conf.py``.

    Examples: ::

        :issue:`123`
        :issue:`42,45`
    """
    options = options or {}
    content = content or []
    issue_nos = [each.strip() for each in utils.unescape(text).split(',')]
    config = inliner.document.settings.env.app.config
    ret = []
    for i, issue_no in enumerate(issue_nos):
        node = make_node(issue_no, config, options=options)
        ret.append(node)
        if i != len(issue_nos) - 1:
            sep = nodes.raw(text=', ', format='html')
            ret.append(sep)
    return ret, []


def setup(app):
    # Base URI setting,
    # e.g. 'https://github.com/sloria/marshmallow/issues/{issue}
    app.add_config_value('issues_uri', default=None, rebuild='html')
    # Shortcut for Github, e.g. 'sloria/marshmallow'
    app.add_config_value('issues_github_path', default=None, rebuild='html')
    app.add_role('issue', issue_role)
