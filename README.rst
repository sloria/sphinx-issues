=============
sphinx-issues
=============

.. image:: https://travis-ci.org/sloria/sphinx-issues.svg?branch=master
    :target: https://travis-ci.org/sloria/sphinx-issues

A Sphinx extension for linking to your project's issue tracker. Includes roles for linking to both issues and user profiles, with built-in support for GitHub (though this works with other services).

Example
*******

For an example usage, check out `marshmallow's changelog <http://marshmallow.readthedocs.org/en/latest/changelog.html#changelog>`_, which makes use of the roles in this library.

Installation and Configuration
******************************
::

    $ pip install sphinx-issues

Add ``sphinx_issues`` to ``extensions`` in your ``conf.py``. If your project is on Github, add the ``issues_github_path`` config variable. Otherwise, use ``issues_uri``.

.. code-block:: python

    # docs/conf.py

    #...
    extensions = [
        #...
        'sphinx_issues',
    ]

    # Github repo
    issues_github_path = 'sloria/marshmallow'

    # equivalent to
    issues_uri = 'https://github.com/sloria/marshmallow/issues/{issue}'

Usage
*****

Use the ``:issue:`` role in your docs like so:

.. code-block:: rst

    See issue :issue:`42`

    See issues :issue:`12,13`


Use the ``:user:`` role in your docs to link to user profiles (Github by default, but can be configured via the ``issues_user_uri`` config variable).

.. code-block:: rst

    Thanks to :user:`bitprophet` for the idea!

You can also use explicit names if you want to use a different name than the github user name:

.. code-block:: rst

    This change is due to :user:`Andreas Mueller <amueller>`.

Credits
*******

Credit goes to Jeff Forcier for his work on the `releases <https://github.com/bitprophet/releases>`_ extension, which is a full-featured solution for generating changelogs. I just needed a quick way to reference Github issues in my docs, so I yoinked the bits that I needed.

License
*******

MIT licensed. See the bundled `LICENSE <https://github.com/sloria/sphinx-issues/blob/master/LICENSE>`_ file for more details.


Changelog
*********

0.3.0 (2016-10-20)
------------------

- Support anchor text for ``:user:`` role. Thanks @jnothman for the suggestion and thanks @amueller for the PR.

0.2.0 (2014-12-22)
------------------

- Add ``:user:`` role for linking to Github user profiles.

0.1.0 (2014-12-21)
------------------

- Initial release.
