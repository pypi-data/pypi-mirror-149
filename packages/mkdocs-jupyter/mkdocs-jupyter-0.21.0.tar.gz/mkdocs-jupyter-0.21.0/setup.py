# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_jupyter',
 'mkdocs_jupyter.tests',
 'mkdocs_jupyter.tests.mkdocs.docs',
 'mkdocs_jupyter.tests.mkdocs.extras']

package_data = \
{'': ['*'],
 'mkdocs_jupyter': ['templates/mkdocs_html/*',
                    'templates/mkdocs_html/assets/*',
                    'templates/mkdocs_md/*'],
 'mkdocs_jupyter.tests': ['mkdocs/*', 'mkdocs/overrides/*'],
 'mkdocs_jupyter.tests.mkdocs.docs': ['img/*']}

install_requires = \
['Pygments>=2.12.0,<3.0.0',
 'jupytext>=1.13.8,<2.0.0',
 'mkdocs-material>=8.0.0,<9.0.0',
 'mkdocs>=1.2.3,<2.0.0',
 'nbconvert>=6.2.0,<7.0.0']

entry_points = \
{'mkdocs.plugins': ['mkdocs-jupyter = mkdocs_jupyter.plugin:Plugin']}

setup_kwargs = {
    'name': 'mkdocs-jupyter',
    'version': '0.21.0',
    'description': 'Use Jupyter in mkdocs websites',
    'long_description': '<p align="center">\n    <img src="https://raw.githubusercontent.com/danielfrg/mkdocs-jupyter/main/docs/logo.png" width="450px">\n</p>\n\n<p align="center">\n    <a href="https://pypi.org/project/mkdocs-jupyter/">\n        <img src="https://badge.fury.io/py/mkdocs-jupyter.svg">\n    </a>\n    <a href="https://github.com/danielfrg/mkdocs-jupyter/actions/workflows/test.yml">\n        <img src="https://github.com/danielfrg/mkdocs-jupyter/workflows/test/badge.svg">\n    </a>\n    <a href="https://codecov.io/gh/danielfrg/mkdocs-jupyter?branch=main">\n        <img src="https://codecov.io/gh/danielfrg/mkdocs-jupyter/branch/main/graph/badge.svg">\n    </a>\n    <a href="http://github.com/danielfrg/mkdocs-jupyter/blob/main/LICENSE.txt">\n        <img src="https://img.shields.io/:license-Apache%202-blue.svg">\n    </a>\n</p>\n\n# mkdocs-jupyter: Use Jupyter Notebooks in mkdocs\n\n- Add Jupyter Notebooks directly to the mkdocs navigation\n- Support for multiple formats:\n  - `.ipynb` and `.py` files (using [jupytext](https://github.com/mwouts/jupytext))\n- Same style as regular Jupyter Notebooks\n  - Support Jupyter Themes\n- Option to execute the notebook before converting\n- Support for [ipywidgets](https://github.com/jupyter-widgets/ipywidgets)\n- Support for mkdocs TOC\n- Option to include notebook source\n\n\n\n<a href="https://raw.githubusercontent.com/danielfrg/mkdocs-jupyter/master/docs/mkdocs-theme.png"><img src="https://raw.githubusercontent.com/danielfrg/mkdocs-jupyter/master/docs/mkdocs-theme.png" alt="mkdocs-jupyter default theme"  width="410"></a>\n<a href="https://raw.githubusercontent.com/danielfrg/mkdocs-jupyter/master/docs/material-theme.png"><img src="https://raw.githubusercontent.com/danielfrg/mkdocs-jupyter/master/docs/material-theme.png" alt="mkdocs-jupyter material theme"  width="410"></a>\n\n## Demo website\n\n[Visit mkdocs-jupyter.danielfrg.com](https://mkdocs-jupyter.danielfrg.com/)\n\n## Installation\n\n```shell\npip install mkdocs-jupyter\n```\n\n## Configuration\n\nIn the `mkdocs.yml` use Jupyter notebooks (`.ipynb`) or Python scripts (`.py`) as pages:\n\n```yaml\nnav:\n- Home: index.md\n- Notebook page: notebook.ipynb\n- Python file: python_script.py\n\nplugins:\n  - mkdocs-jupyter\n```\n\n### Titles and Table of Contents\n\nThe first h1 header (`#`) in your notebook will be used as the title.\n\n```md\n# This H1 header will be the the title.\n```\n\nThis can be turned off in the configuration (in which case the filename will be used as title):\n\n```yaml\nplugins:\n  - mkdocs-jupyter:\n      ignore_h1_titles: True\n```\n\nIn order to see the table of contents you need to maintain a hierarchical headers structure in your notebooks.\nYou must use h2 headers (`##`) and not h1 (`#`)\n\n```md\n## This H2 title will show in the table of contents\n```\n\nIf you want to **nest headers** in the TOC you need to add additional levels later\nin the same markdown cell or new bottom markdown cells:\n\n```md\n## This header will show as top level in the table of contents\n\n<content>\n\n### This one will be displayed inside the above level\n```\n\n### Including or Ignoring Files\n\nYou can control which files are included or ignored via lists of glob patterns:\n\n```yaml\nplugins:\n  - mkdocs-jupyter:\n      include: ["*.ipynb"]  # Default: ["*.py", "*.ipynb"]\n      ignore: ["some-irrelevant-files/*.ipynb"]\n```\n\n### Execute Notebook\n\nYou can tell the plugin to execute the notebook before converting, default is `False`:\n\n```yaml\nplugins:\n  - mkdocs-jupyter:\n      execute: True\n```\n\nYou can tell the plugin to ignore the execution of some files (with glob matching):\n\n```yaml\nplugins:\n  - mkdocs-jupyter:\n      execute_ignore: "my-secret-files/*.ipynb"\n```\n\nTo fail when notebook execution fails set `allow_errors` to `false`:\n\n```yaml\nplugins:\n  - mkdocs-jupyter:\n      execute: true\n      allow_errors: false\n```\n\n#### Kernel\n\nBy default the plugin will use the kernel specified in the notebook to execute it.\nYou can specify a custom kernel name to use for all the notebooks:\n\n```yaml\nplugins:\n  - mkdocs-jupyter:\n      kernel_name: python3\n```\n\n### Jupyter themes\n\nYou can configure the different Jupyter themes.\nFor example if using material with `slate` color scheme you can use the Jupyter Lab `dark` theme:\n\n```yml\nplugins:\n  - mkdocs-jupyter:\n      theme: dark\n\ntheme:\n  name: material\n  palette:\n    scheme: slate\n```\n\n### Download notebook link\n\nYou can tell the plugin to include the notebook source to make it easy to show\na download button in the theme, default is `False`:\n\n```yml\nplugins:\n  - mkdocs-jupyter:\n      include_source: True\n```\n\nThis setting will also create a `page.nb_url` value that you can use in your theme\nto make a link in each page.\n\nFor example in `mkdocs-material`\n(see [customization](https://squidfunk.github.io/mkdocs-material/customization/#overriding-template-blocks)),\nyou can create a `main.html` file like this:\n\n```jinja\n{% extends "base.html" %}\n\n{% block content %}\n{% if page.nb_url %}\n    <a href="{{ page.nb_url }}" title="Download Notebook" class="md-content__button md-icon">\n        {% include ".icons/material/download.svg" %}\n    </a>\n{% endif %}\n\n{{ super() }}\n{% endblock content %}\n```\n\n![Download Notebook button](https://raw.githubusercontent.com/danielfrg/mkdocs-jupyter/master/docs/download-button.png)\n\n### Styles\n\nThis extensions includes the Jupyter Lab nbconvert CSS styles and does some changes\nto make it as generic as possible in order for it to work with a variety of mkdocs themes.\nThis is not always possible and the theme we test the most is [mkdocs-material](https://squidfunk.github.io/mkdocs-material).\n\nIt\'s possible you might need to do some CSS changes to make it look as good as you\nwant, for example for the material theme take a look at their [customization docs](https://squidfunk.github.io/mkdocs-material/customization/#overriding-template-blocks).\n\nCreate a `main.html` file like:\n\n```jinja\n{% extends "base.html" %}\n\n{% block content %}\n{{ super() }}\n\n<style>\n// Do whatever changes you need here\n\n.jp-RenderedHTMLCommon p {\n    color: red\n}\n\n</style>\n{% endblock content %}\n```\n',
    'author': 'Daniel Rodriguez',
    'author_email': 'None',
    'maintainer': 'Daniel Rodriguez',
    'maintainer_email': 'None',
    'url': 'https://github.com/danielfrg/mkdocs-jupyter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
