import pathlib
import sys

_TOP_DIRECTORY = pathlib.Path(__file__).parent.parent
assert _TOP_DIRECTORY.is_dir()
assert (_TOP_DIRECTORY / "pytest.ini").is_file()
sys.path.insert(0, str(_TOP_DIRECTORY))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Octoprobe: testbed_tutorial"
copyright = "2024, Hans Märki"
author = "Hans Märki"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "myst_parser",
    # "sphinx.ext.napoleon",
]

default_role = "code"
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
