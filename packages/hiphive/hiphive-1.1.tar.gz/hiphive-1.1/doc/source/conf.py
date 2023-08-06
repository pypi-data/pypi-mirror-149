#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath('../../hiphive'))
sys.path.insert(0, os.path.abspath('../../hiphive/trainstation'))
sys.path.insert(0, os.path.abspath('../../hiphive/calculators'))
sys.path.insert(0, os.path.abspath('../../hiphive/io'))
sys.path.insert(0, os.path.abspath('../../hiphive/core'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.graphviz',
    'sphinx_autodoc_typehints',
    'sphinx_sitemap',
    'cloud_sptheme.ext.table_styling',
    'nbsphinx']

graphviz_output_format = 'svg'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
pygments_style = 'sphinx'
todo_include_todos = True

# Collect basic information from main module
with open('../../hiphive/__init__.py') as fd:
    lines = '\n'.join(fd.readlines())
version = ''
if len(version) == 0:
    version = re.search("__version__ = '(.*)'", lines).group(1)
release = ''
copyright = re.search("__copyright__ = '(.*)'", lines).group(1)
project = re.search("__project__ = '(.*)'", lines).group(1)
author = re.search("__maintainer__ = '(.*)'", lines).group(1)

site_url = 'https://hiphive.materialsmodeling.org'
html_logo = "_static/logo.png"
html_favicon = "_static/logo.ico"
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']
html_theme_options = {'display_version': True}
html_context = {
    'current_version': version,
    'versions':
        [('latest stable release',
          '{}'.format(site_url)),
         ('development version',
          '{}/dev'.format(site_url))]}
htmlhelp_basename = 'hiPhivedoc'
intersphinx_mapping = \
    {'ase':     ('https://wiki.fysik.dtu.dk/ase', None),
     'numpy':   ('https://numpy.org/doc/stable/', None),
     'h5py':    ('http://docs.h5py.org/en/latest/', None),
     'scipy':   ('https://scipy.github.io/devdocs/', None),
     'sklearn': ('https://scikit-learn.org/stable', None),
     'trainstation': ('https://trainstation.materialsmodeling.org/', None)}

# Settings for nbsphinx
nbsphinx_execute = 'never'

# Options for LaTeX output
_PREAMBLE = r"""
\usepackage{amsmath,amssymb}
\renewcommand{\vec}[1]{\boldsymbol{#1}}
\DeclareMathOperator*{\argmin}{\arg\!\min}
\DeclareMathOperator{\argmin}{\arg\!\min}
"""

latex_elements = {
    'preamble': _PREAMBLE,
}
latex_documents = [
    (master_doc, 'hiPhive.tex', 'hiPhive Documentation',
     'The hiPhive developer team', 'manual'),
]


# Options for manual page output
man_pages = [
    (master_doc, 'hiPhive', 'hiPhive Documentation',
     [author], 1)
]


# Options for Texinfo output
texinfo_documents = [
    (master_doc, 'hiPhive', 'hiPhive Documentation',
     author, 'hiPhive', 'Higher order force constants for everyone',
     'Miscellaneous'),
]


html_css_files = [
    'custom.css',
]
