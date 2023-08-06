# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['examples', 'functimer', 'tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'functimer',
    'version': '1.3.1',
    'description': 'A programmatic approach to function runtime estimation.',
    'long_description': '# functimer\n\nA programmatic approach to function runtime estimation.\n\n[![PyPI version](https://badge.fury.io/py/functimer.svg)](https://badge.fury.io/py/functimer)\n[![codecov](https://codecov.io/gh/EJEmmett/functimer/branch/master/graph/badge.svg?token=L0UMBK8AD4)](https://codecov.io/gh/EJEmmett/functimer)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/EJEmmett/functimer.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/EJEmmett/functimer/context:python)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/857af82e6ff14a68b5bf0866e0b44d30)](https://www.codacy.com/gh/EJEmmett/functimer/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=EJEmmett/functimer&amp;utm_campaign=Badge_Grade)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n---\n\n## About\nThis package first came about as a way to serve my needs during an Algorithms class in college.<br/>\nIt started as a function that stored time elapsed results in a global dictionary, where the key was a tuple of the functions name and return value.\nNow it\'s just a bit different. \n\n\n\n## Installation\n- PYPI:\n    ```shell\n        pip install functimer\n    ```\n\n- Manual:\n    ```shell\n        poetry install --no-dev\n        poetry build\n        pip install dist/*.whl\n    ```\n\n\nHow to install [Poetry](https://python-poetry.org/docs/#installation).\n\n## Quick Example\n### Comprehensive Examples in `examples/`\n\n- Python\n  ```py\n      @timed(unit=Unit.SECOND, number=1)\n      def timed_sleep(seconds):\n          sleep(seconds)\n\n      runtime = timed_sleep(1)\n      "1.00 s"\n  ```\n\n- Command Line\n  ```shell\n    $ python -m functimer "sum([1, 2, 3])"\n    Average runtime of 10,000 executions: 0.15 µs\n\n    $ python -m functimer "sum([1, 2, 3])" --return\n    Average runtime of 10,000 executions: 0.15 µs\n    sum([1, 2, 3]) -> 6\n\n    $ python -m functimer "(lambda x: x+x)(10)" --return\n    Average runtime of 10,000 executions: 0.14 µs\n    (lambda x: x+x)(10) -> 20\n\n    $ python -m functimer "functimer.util.get_unit(\'1.00 s\')" --return\n    Average runtime of 10,000 executions: 0.50 µs\n    functimer.util.get_unit(\'1.00 s\') -> Unit.SECOND\n\n    $ python -m functimer "functimer.classes.Unit.from_str(\'s\')" --return\n    Average runtime of 10,000 executions: 0.25 µs\n    functimer.classes.Unit.from_str(\'s\') -> Unit.SECOND\n  ```\n\n### Tests\nRun `tox` in the root directory of the repo.\n\n### License\nMIT\n',
    'author': 'Edward Emmett',
    'author_email': 'edemms12@gmail.com',
    'maintainer': 'Edward Emmett',
    'maintainer_email': 'edemms12@gmail.com',
    'url': 'https://github.com/EJEmmett/functimer',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
