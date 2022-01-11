# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "sphinx-issues"
copyright = "2022, foobar"
author = "foobar"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx_issues"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

#
suppress_warnings = ["app.add_node"]

issues_uri = "https://gitlab.company.com/{group}/{project}/-/issues/{issue}"
issues_prefix = "#"
issues_pr_uri = "https://gitlab.company.com/{group}/{project}/-/merge_requests/{pr}"
issues_pr_prefix = "!"
issues_commit_uri = "https://gitlab.company.com/{group}/{project}/-/commit/{commit}"
issues_commit_prefix = "@"
issues_user_uri = "https://gitlab.company.com/{user}"
issues_user_prefix = "@"
issues_default_group_project = "myteam/super_great_project"
