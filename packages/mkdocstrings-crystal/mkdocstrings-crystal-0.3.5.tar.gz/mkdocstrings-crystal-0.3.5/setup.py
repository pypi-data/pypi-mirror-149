# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocstrings', 'mkdocstrings.handlers.crystal']

package_data = \
{'': ['*'], 'mkdocstrings': ['templates/crystal/material/*']}

install_requires = \
['Jinja2>=2.11.2,<4.0',
 'cached-property',
 'markdown-callouts>=0.1.0',
 'markupsafe>=1.1.1,<3.0',
 'mkdocs-autorefs>=0.2.0',
 'mkdocstrings>=0.15.1']

entry_points = \
{'markdown.extensions': ['deduplicate-toc = '
                         'mkdocstrings.handlers.crystal.deduplicate_toc:DeduplicateTocExtension']}

setup_kwargs = {
    'name': 'mkdocstrings-crystal',
    'version': '0.3.5',
    'description': 'Crystal language doc generator for mkdocstrings',
    'long_description': "# mkdocstrings-crystal\n\n**[Crystal][] language doc generator for [MkDocs][], via [mkdocstrings][]**\n\n[![PyPI](https://img.shields.io/pypi/v/mkdocstrings-crystal)](https://pypi.org/project/mkdocstrings-crystal/)\n[![GitHub](https://img.shields.io/github/license/oprypin/mkdocstrings-crystal)](https://github.com/mkdocstrings/crystal/blob/master/LICENSE.md)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/oprypin/mkdocstrings-crystal/CI)](https://github.com/mkdocstrings/crystal/actions?query=event%3Apush+branch%3Amaster)\n\n## Introduction\n\n*mkdocstrings-crystal* allows you to insert API documentation (generated from [Crystal][]'s source code and doc comments) as part of any page on a [MkDocs][] site.\n\n[See it in action][showcase].\n\nTo install it, run (possibly in a [virtualenv][]):\n\n```shell\npip install mkdocstrings-crystal\n```\n\n**Continue to the [documentation site][].**\n\n## Usage\n\nWith [MkDocs][], add/merge this base config as your _mkdocs.yml_:\n\n```yaml\nsite_name: My Project\n\ntheme:\n  name: material\n\nplugins:\n  - search\n  - mkdocstrings:\n      default_handler: crystal\n\nmarkdown_extensions:\n  - pymdownx.highlight\n  - deduplicate-toc\n```\n\nThen, in any `docs/**/*.md` file, you can **mention a Crystal identifier alone on a line, after `:::`**:\n\n```md\n::: MyClass\n\n::: Other::Class#some_method\n\n::: Foo::CONSTANT\n```\n\n-- and in the output this will be replaced with generated API documentation for it, much like Crystal's own doc generator does.\n\nThis, of course, happens as part of a normal MkDocs build process:\n\n```shell\nmkdocs build  # generate from docs/ into site/\nmkdocs serve  # live preview\n```\n\n**Continue to the [documentation site][].**\n\n\n[crystal]: https://crystal-lang.org/\n[mkdocs]: https://www.mkdocs.org/\n[mkdocstrings]: https://mkdocstrings.github.io/\n[virtualenv]: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment\n[documentation site]: https://mkdocstrings.github.io/crystal/\n[showcase]: https://mkdocstrings.github.io/crystal/showcase.html\n",
    'author': 'Oleh Prypin',
    'author_email': 'oleh@pryp.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mkdocstrings/crystal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
