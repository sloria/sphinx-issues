=============
sphinx-issues
=============

A Sphinx extension for linking to your project's issue tracker.

Installation and Configuration
------------------------------
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
-----

Use the ``:issue:`` role in your docs like so:

.. code-block:: rst

    See issue :issue:`42`

    See issues :issue:`12,13`

Credits
-------

Credit goes to Jeff Forcier for his work on the `releases <https://github.com/bitprophet/releases>`_ extension, which is a full-featured solution for generating changelogs. I just needed a quick way to reference Github issues in my docs, so I yoinked the bits that I needed.

License
-------

MIT licensed. See the bundled `LICENSE <https://github.com/sloria/sphinx-issues/blob/master/LICENSE>`_ file for more details.


Changelog
---------

0.1.0
-----

- Initial release.
