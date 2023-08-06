# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calligraphy_scripting', 'calligraphy_scripting.data']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['calligraphy = calligraphy_scripting.cli:cli']}

setup_kwargs = {
    'name': 'calligraphy-scripting',
    'version': '1.1.2',
    'description': 'A hybrid language for a modern approach to shell scripting',
    'long_description': "# Calligraphy\n---\n[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![CI](https://github.com/jfcarter2358/calligraphy/actions/workflows/makefile.yml/badge.svg)](https://github.com/jfcarter2358/calligraphy/actions/workflows/makefile.yml)\n![Coverage Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/jfcarter2358/a5b95abd1dc360c13da66165ff482d5e/raw/calligraphy__heads_main.json)\n\n**Shell scripting for the modern age**\n\nCalligraphy is a hybrid scripting language that allows you to mix Python and Bash code\nin the same file. This gives you the advantages of bash when working with other\nprocesses while also giving you the advantages of a modern language like Python.\n\nIt's a free software distributed under the MIT Licence unless\notherwise specified.\n\nDevelopment is hosted on GitHub: https://github.com/jfcarter2358/calligraphy/\n\nPull requests are amazing and most welcome.\n\n## Install\n\nCalligraphy can be simply installed by running\n\n```\npip install calligraphy-scripting\n```\n\nIf you want to install from a source distribution, extract the tarball and run\nthe following command (this requires poetry to be installed)\n\n```\npoetry install --no-dev\n```\n\n## Documentation\n\nThe documentation lives at https://calligraphy.readthedocs.io/.\n\n## Testing\n\nWe use `pytest` and `pytest-cov` for running the test suite. You should be able to install them with\n\n```\npip install pytest pytest-cov\n```\n\nor you can install calligraphy alongside those packages with\n\n```\npoetry install\n```\n\nTo run the test suite, you can do\n\n```\nmake test\n```\n\nThis will produce an html coverage report under the `htmlcov` directory.\n\n## Roadmap\n\nYou can find the Calligraphy roadmap [here](https://jfcarter2358.notion.site/5081d4214297401db15a43e47a974521?v=9858c59c7ecd4eefa09bf75158c47448)\n\n## License\n\nCalligraphy is under the [MIT license](https://opensource.org/licenses/MIT).\n\n## Contact\n\nIf you have any questions or concerns please reach out to me (John Carter) at [jfcarter2358@gmail.com](mailto:jfcarter2358@gmail.com)\n",
    'author': 'John Carter',
    'author_email': 'jfcarter2358@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jfcarter2358/calligraphy',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
