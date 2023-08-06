# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['euporie',
 'euporie.app',
 'euporie.commands',
 'euporie.convert',
 'euporie.convert.formats',
 'euporie.formatted_text',
 'euporie.key_binding',
 'euporie.key_binding.bindings',
 'euporie.tabs',
 'euporie.widgets',
 'euporie.widgets.output']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0,<10.0',
 'Pygments>=2.11.2,<3.0.0',
 'aenum>=3.1,<4.0',
 'appdirs>=1.4,<2.0',
 'flatlatex>=0.15,<0.16',
 'html2text>=2020.1.16,<2021.0.0',
 'imagesize>=1.3.0,<2.0.0',
 'jsonschema>=4.4,<5.0',
 'jupyter-client>=7.1,<8.0',
 'linkify>=1.4,<2.0',
 'markdown-it-py[linkify]>=2.0.1,<3.0.0',
 'mdit-py-plugins>=0.3.0,<0.4.0',
 'nbformat>=5,<6',
 'prompt-toolkit>=3.0.27,<4.0.0',
 'pyperclip>=1.8,<2.0',
 'timg>=1.1,<2.0']

extras_require = \
{':extra == "all" or extra == "hub"': ['asyncssh[hub]>=2.10.1,<3.0.0'],
 'all': ['black>=19.3b0',
         'isort>=5.10.1,<6.0.0',
         'ssort>=0.11.4,<0.12.0',
         'CairoSVG>=2.5,<3.0'],
 'formatters': ['black>=19.3b0',
                'isort>=5.10.1,<6.0.0',
                'ssort>=0.11.4,<0.12.0'],
 'html-mtable': ['mtable>=0.1,<0.2', 'html5lib>=1.1,<2.0'],
 'images-img2unicode': ['img2unicode>=0.1a8,<0.2'],
 'latex-sympy': ['sympy>=1.9,<2.0', 'antlr4-python3-runtime>=4.9,<5.0'],
 'svg-cairosvg': ['CairoSVG>=2.5,<3.0']}

entry_points = \
{'console_scripts': ['euporie = euporie.__main__:main']}

setup_kwargs = {
    'name': 'euporie',
    'version': '1.6.1',
    'description': 'Euporie is a text-based user interface for running and editing Jupyter notebooks',
    'long_description': '|logo|\n\n.. |logo| image:: https://user-images.githubusercontent.com/12154190/160670889-c6fc4cd8-413d-49f0-b105-9c0e03117032.svg\n   :alt: <Logo>\n\n#######\neuporie\n#######\n\n|PyPI| |RTD| |PyVer| |License| |Binder| |Stars|\n\n.. content_start\n\n**Euporie is a terminal app for running and editing Jupyter notebooks.**\n\nThe text-based interface is inspired by JupyterLab / Jupyter Notebook, and runs entirely in the terminal.\n\n.. figure:: https://user-images.githubusercontent.com/12154190/165388661-44153d99-a44b-4a4a-98b8-7007158c3fa3.png\n   :target: https://user-images.githubusercontent.com/12154190/165388661-44153d99-a44b-4a4a-98b8-7007158c3fa3.png\n\n   `View more screenshots here <https://euporie.readthedocs.io/en/latest/pages/gallery.html>`_\n\n----\n\n*******\nInstall\n*******\n\nYou can install euporie with `pipx <https://pipxproject.github.io/>`_ (recommended) or ``pip``:\n\n.. code-block:: console\n\n   $ pipx install euporie\n   $ # OR\n   $ python -m pip install --user euporie\n\nYou can also try euporie online `here <https://mybinder.org/v2/gh/joouha/euporie-binder/HEAD?urlpath=%2Feuporie%2F>`_.\n\n*****\nUsage\n*****\n\nOpen a notebook using the ``edit`` subcommand and passing the notebook\'s file path as a command line argument:\n\n.. code-block:: console\n\n   $ euporie edit notebook.ipynb\n\nAlternatively, launch ``euporie`` and open a notebook file by selecting "Open" from the file menu (*Ctrl+o*).\n\nTo print a notebook to the terminal, use the ``preview`` subcommand:\n\n.. code-block:: console\n\n   $ euporie preview notebook.ipynb\n\nTo view a notebook in the system pager, use the ``--page`` flag:\n\n.. code-block:: console\n\n   $ euporie preview --page notebook.ipynb\n\nFor more information about the available subcommands and command line flags, run:\n\n.. code-block:: console\n\n   $ euporie --help\n\n\n*************\nDocumentation\n*************\n\nView the online documentation at: `https://euporie.readthedocs.io/ <https://euporie.readthedocs.io/>`_\n\nThe code is available on GitHub at: `https://github.com/joouha/euporie <https://github.com/joouha/euporie>`_\n\n********\nFeatures\n********\n\n* Edit and run notebooks in the terminal\n* Displays rich cell outputs, including markdown, tables, images, LaTeX, HTML, SVG, & PDF\n* Print formatted notebooks to the terminal or pager\n* Open multiple notebooks and display them stacked or tiled\n* Code completion\n* Line completions from history\n* Contextual help\n* Automatic code formatting\n* Highly configurable\n\n\n*************\nCompatibility\n*************\n\nEuporie requires Python 3.8 or later. It works on Linux, Windows and MacOS\n\n\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/euporie.svg\n    :target: https://pypi.python.org/project/euporie/\n    :alt: Latest Version\n\n.. |RTD| image:: https://readthedocs.org/projects/euporie/badge/\n    :target: https://euporie.readthedocs.io/en/latest/\n    :alt: Documentation\n\n.. |PyVer| image:: https://img.shields.io/pypi/pyversions/euporie\n    :target: https://pypi.python.org/project/euporie/\n    :alt: Supported Python versions\n\n.. |Binder| image:: https://mybinder.org/badge_logo.svg\n   :target: https://mybinder.org/v2/gh/joouha/euporie-binder/HEAD?urlpath=%2Feuporie%2F\n   :alt: Launch with Binder\n\n.. |License| image:: https://img.shields.io/github/license/joouha/euporie.svg\n    :target: https://github.com/joouha/euporie/blob/main/LICENSE\n    :alt: View license\n\n.. |Stars| image:: https://img.shields.io/github/stars/joouha/euporie\n    :target: https://github.com/joouha/euporie/stargazers\n    :alt: ⭐\n',
    'author': 'Josiah Outram Halstead',
    'author_email': 'josiah@halstead.email',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joouha/euporie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
