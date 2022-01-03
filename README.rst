=============
sphinx-issues
=============

.. image:: https://badgen.net/pypi/v/sphinx-issues
  :alt: pypi badge
  :target: https://pypi.org/project/sphinx-issues/

.. image:: https://badgen.net/travis/sloria/sphinx-issues
  :alt: travis-ci status
  :target: https://travis-ci.org/sloria/sphinx-issues

.. image:: https://badgen.net/badge/code%20style/black/000
   :target: https://github.com/ambv/black
   :alt: Code style: Black

A Sphinx extension for linking to your project's issue tracker. Includes roles for linking to issues, pull requests, user profiles, with built-in support for GitHub (though this works with other services).

Example
*******

For an example usage, check out `marshmallow's changelog <http://marshmallow.readthedocs.org/en/latest/changelog.html>`_, which makes use of the roles in this library.

Installation and Configuration
******************************

.. code-block:: console

    pip install sphinx-issues


Add ``sphinx_issues`` to ``extensions`` in your ``conf.py``. If your project is on GitHub, add the ``issues_github_path`` config variable.
Otherwise, use ``issues_uri``, ``issues_pr_uri``, and ``issues_commit_uri``.

.. code-block:: python

    # docs/conf.py

    # ...
    extensions = [
        # ...
        "sphinx_issues"
    ]

    # GitHub repo
    issues_github_path = "sloria/marshmallow"

    # equivalent to
    issues_uri = "https://github.com/sloria/marshmallow/issues/{issue}"
    issues_pr_uri = "https://github.com/sloria/marshmallow/pull/{pr}"
    issues_commit_uri = "https://github.com/sloria/marshmallow/commit/{commit}"

Usage
*****

Use the ``:issue:``  and ``:pr:`` roles in your docs like so:

.. code-block:: rst

    See issue :issue:`42`

    See issues :issue:`12,13`

    See :issue:`sloria/konch#45`.

    See PR :pr:`58`


Use the ``:user:`` role in your docs to link to user profiles (GitHub by default, but can be configured via the ``issues_user_uri`` config variable).

.. code-block:: rst

    Thanks to :user:`bitprophet` for the idea!

You can also use explicit names if you want to use a different name than the github user name:

.. code-block:: rst

    This change is due to :user:`Andreas Mueller <amueller>`.


Use the ``:commit:`` role to link to commits.

.. code-block:: rst

    Fixed in :commit:`6bb9124d5e9dbb2f7b52864c3d8af7feb1b69403`.

Use the ``:cve:`` role to link to CVEs on https://cve.mitre.org.

.. code-block:: rst

    :cve:`CVE-2018-17175` - Addresses possible vulnerability when...

Use the ``:cwe:`` role to link to CWEs on https://cwe.mitre.org.

.. code-block:: rst

    :cwe:`CWE-787` - The software writes data past the end, or...

Credits
*******

Credit goes to Jeff Forcier for his work on the `releases <https://github.com/bitprophet/releases>`_ extension, which is a full-featured solution for generating changelogs. I just needed a quick way to reference GitHub issues in my docs, so I yoinked the bits that I needed.

License
*******

MIT licensed. See the bundled `LICENSE <https://github.com/sloria/sphinx-issues/blob/master/LICENSE>`_ file for more details.


Changelog
*********

2.0.0 (2022-01-01)
------------------

- Drop support for Python 2.7 and 3.5.
- Test against Python 3.8 to 3.10.
- Add ``:cwe:`` role for linking to CVEs on https://cwe.mitre.org.
  Thanks @hugovk for the PR.

1.2.0 (2018-12-26)
------------------

- Add ``:commit:`` role for linking to commits.
- Add support for linking to external repos.
- Test against Python 3.7.

1.1.0 (2018-09-18)
------------------

- Add ``:cve:`` role for linking to CVEs on https://cve.mitre.org.

1.0.0 (2018-07-14)
------------------

- Add ``:pr:`` role. Thanks @jnotham for the suggestion.
- Drop support for Python 3.4.

0.4.0 (2017-11-25)
------------------

- Raise ``ValueError`` if neither ``issues_uri`` nor ``issues_github_path`` is set. Thanks @jnothman for the PR.
- Drop support for Python 2.6 and 3.3.

0.3.1 (2017-01-16)
------------------

- ``setup`` returns metadata, preventing warnings about parallel reads and writes. Thanks @jfinkels for reporting.

0.3.0 (2016-10-20)
------------------

- Support anchor text for ``:user:`` role. Thanks @jnothman for the suggestion and thanks @amueller for the PR.

0.2.0 (2014-12-22)
------------------

- Add ``:user:`` role for linking to GitHub user profiles.

0.1.0 (2014-12-21)
------------------

- Initial release.
