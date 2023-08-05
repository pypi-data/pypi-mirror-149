# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sphinx_artisan_theme', 'sphinx_artisan_theme.ext']

package_data = \
{'': ['*'],
 'sphinx_artisan_theme': ['themes/artisan/*', 'themes/artisan/static/*']}

install_requires = \
['Sphinx>=4.4.0,<5.0.0']

entry_points = \
{'sphinx.html_themes': ['sphinx_artisan_theme = sphinx_artisan_theme']}

setup_kwargs = {
    'name': 'sphinx-artisan-theme',
    'version': '0.0.1b2',
    'description': '',
    'long_description': '# Artisan Sphinx Theme\n\n<p class="lead">\nAn elegant theme designed to style the sphinx documentation for all Artisan of\nCode projects.\n</p>\n\n\n## 🛠 Installing\n\n```\npoetry add sphinx-artisan-theme\n```\n\n## 📚 Help\n\nSee the [Documentation][docs] or ask questions on the [Discussion][discussions] board.\n\n## ⚖️ Licence\n\nThis project is licensed under the [MIT licence][mit_licence].\n\nAll documentation and images are licenced under the \n[Creative Commons Attribution-ShareAlike 4.0 International License][cc_by_sa].\n\n## 📝 Meta\n\nThis project uses [Semantic Versioning][semvar].\n\n[docs]: https://sphinx-artisan-theme.artisan.io\n[discussions]: https://github.com/artisanofcode/sphinx-artisan-theme/discussions\n[mit_licence]: http://dan.mit-license.org/\n[cc_by_sa]: https://creativecommons.org/licenses/by-sa/4.0/\n[semvar]: http://semver.org/\n',
    'author': 'Daniel Knell',
    'author_email': 'contact@danielknell.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
