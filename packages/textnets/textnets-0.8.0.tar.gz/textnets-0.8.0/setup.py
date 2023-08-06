# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textnets']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.24,<0.30.0',
 'igraph>=0.9.7,<0.10.0,!=0.9.9,!=0.9.10',
 'leidenalg>=0.8.9,<0.9.0',
 'pandas>=1.4.0,<2.0.0',
 'scipy>=1.7.0,<2.0.0',
 'spacy>=3.3.0,<4.0.0',
 'toolz>=0.11.1,<0.12.0',
 'wasabi>=0.9.1,<0.10.0']

extras_require = \
{':sys_platform == "linux" or sys_platform == "darwin"': ['cairocffi>=1.3.0,<2.0.0'],
 ':sys_platform == "win32"': ['pycairo>=1.21.0,<2.0.0'],
 'doc': ['jupyter-sphinx>=0.3.2,<0.4.0',
         'sphinxcontrib-bibtex>=2.3.0,<3.0.0',
         'Sphinx>=4.0.2,<5.0.0',
         'pydata-sphinx-theme>=0.8.0,<0.9.0']}

setup_kwargs = {
    'name': 'textnets',
    'version': '0.8.0',
    'description': 'Automated text analysis with networks',
    'long_description': '=====================================\nTextnets: text analysis with networks\n=====================================\n\n.. image:: https://mybinder.org/badge_logo.svg\n   :target: https://mybinder.org/v2/gh/jboynyc/textnets-binder/trunk?filepath=Tutorial.ipynb\n   :alt: Launch on Binder\n\n.. image:: https://github.com/jboynyc/textnets/actions/workflows/ci.yml/badge.svg\n   :target: https://github.com/jboynyc/textnets/actions/workflows/ci.yml\n   :alt: CI status\n\n.. image:: https://readthedocs.org/projects/textnets/badge/?version=stable\n   :target: https://textnets.readthedocs.io/en/stable/?badge=stable\n   :alt: Documentation Status\n\n.. image:: https://anaconda.org/conda-forge/textnets/badges/installer/conda.svg\n   :target: https://anaconda.org/conda-forge/textnets\n   :alt: Install with conda\n\n.. image:: https://joss.theoj.org/papers/10.21105/joss.02594/status.svg\n   :target: https://doi.org/10.21105/joss.02594\n   :alt: Published in Journal of Open Source Software\n\n**textnets** represents collections of texts as networks of documents and\nwords. This provides novel possibilities for the visualization and analysis of\ntexts.\n\n.. figure:: https://textnets.readthedocs.io/en/dev/_static/impeachment-statements.svg\n   :alt: Bipartite network graph\n\n   Network of U.S. Senators and words used in their official statements\n   following the acquittal vote in the 2020 Senate impeachment trial (`source\n   <https://www.jboy.space/blog/enemies-foreign-and-partisan.html>`_).\n\nThe ideas underlying **textnets** are presented in this paper:\n\n  Christopher A. Bail, "`Combining natural language processing and network\n  analysis to examine how advocacy organizations stimulate conversation on social\n  media`__," *Proceedings of the National Academy of Sciences of the United States\n  of America* 113, no. 42 (2016), 11823–11828, doi:10.1073/pnas.1607151113.\n\n__ https://doi.org/10.1073/pnas.1607151113\n\nInitially begun as a Python implementation of `Chris Bail\'s textnets package\nfor R`_, **textnets** now comprises several unique features for term extraction\nand weighing, visualization, and analysis.\n\n.. _`Chris Bail\'s textnets package for R`: https://github.com/cbail/textnets/\n\n**textnets** is free software under the terms of the GNU General Public License\nv3.\n\nFeatures\n--------\n\n**textnets** builds on `spaCy`_, a state-of-the-art library for\nnatural-language processing, and `igraph`_ for network analysis. It uses the\n`Leiden algorithm`_ for community detection, which is able to perform community\ndetection on the bipartite (word–group) network.\n\n.. _`igraph`: http://igraph.org/python/\n.. _`Leiden algorithm`: https://doi.org/10.1038/s41598-019-41695-z\n.. _`spaCy`: https://spacy.io/\n\n**textnets** seamlessly integrates with Python\'s excellent `scientific stack`_.\nThat means that you can use **textnets** to analyze and visualize your data in\nJupyter notebooks!\n\n.. _`scientific stack`: https://numfocus.org/\n\n**textnets** is easily installable using the ``conda`` and ``pip`` package\nmanagers. It requires Python 3.7 or higher.\n\nRead `the documentation <https://textnets.readthedocs.io>`_ to learn more about\nthe package\'s features.\n\nCitation\n--------\n\nUsing **textnets** in a scholarly publication? Please cite this paper:\n\n.. code-block:: bibtex\n\n   @article{Boy2020,\n     author   = {John D. Boy},\n     title    = {textnets},\n     subtitle = {A {P}ython Package for Text Analysis with Networks},\n     journal  = {Journal of Open Source Software},\n     volume   = {5},\n     number   = {54},\n     pages    = {2594},\n     year     = {2020},\n     doi      = {10.21105/joss.02594},\n   }\n\nLearn More\n----------\n\n==================  =============================================\n**Documentation**   https://textnets.readthedocs.io/\n**Repository**      https://github.com/jboynyc/textnets\n**Issues & Ideas**  https://github.com/jboynyc/textnets/issues\n**Conda-Forge**     https://anaconda.org/conda-forge/textnets\n**PyPI**            https://pypi.org/project/textnets/\n**FOSDEM \'22**      https://fosdem.org/2022/schedule/event/open_research_textnets/\n**DOI**             `10.21105/joss.02594 <https://doi.org/10.21105/joss.02594>`_\n**Archive**         `10.5281/zenodo.3866676 <https://doi.org/10.5281/zenodo.3866676>`_\n==================  =============================================\n\n.. image:: https://textnets.readthedocs.io/en/dev/_static/textnets-logo.svg\n   :alt: textnets logo\n   :target: https://textnets.readthedocs.io\n   :align: center\n   :width: 140\n',
    'author': 'John D. Boy',
    'author_email': 'jboy@bius.moe',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://textnets.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.0,<3.11',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
