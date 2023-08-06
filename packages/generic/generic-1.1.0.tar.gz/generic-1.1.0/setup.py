# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['generic']

package_data = \
{'': ['*']}

install_requires = \
['exceptiongroup>=1.0.0-rc.5,<2.0.0']

setup_kwargs = {
    'name': 'generic',
    'version': '1.1.0',
    'description': 'Generic programming library for Python',
    'long_description': '# Generic programming library for Python\n\n[![Build state](https://github.com/gaphor/generic/workflows/build/badge.svg)](https://github.com/gaphor/generic/actions)\n[![Maintainability](https://api.codeclimate.com/v1/badges/c7be2d28400687b1375a/maintainability)](https://codeclimate.com/github/gaphor/generic/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/c7be2d28400687b1375a/test_coverage)](https://codeclimate.com/github/gaphor/generic/test_coverage)\n[![Documentation Status](https://readthedocs.org/projects/generic/badge/?version=latest)](https://generic.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/Gaphor/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n\nGeneric is a library for [Generic programming](https://en.wikipedia.org/wiki/Generic_programming), also known as [Multiple dispatch](https://en.wikipedia.org/wiki/Multiple_dispatch).\n\nThe Generic library supports:\n\n* multi-dispatch: like `functools.singledispatch`, but for more than one parameter\n* multi-methods: multi-dispatch, but for methods\n* event dispatching: based on a hierarchical event structure (event objects)\n\nYou can read\n[documentation](http://generic.readthedocs.org/en/latest/index.html) hosted at\nexcellent readthedocs.org project. Development takes place on\n[github](http://github.com/gaphor/generic).\n\n\n# Changes\n\n## 1.1.0\n\n- Rename `master` branch to `main`\n- `generic.event.Manager` executes all handlers and throws an `ExceptionGroup` in case of errors\n\n## 1.0.1\n\n- Add Support for Python 3.10, Drop Support for Python 3.7\n- Enable Pre-commit Hooks for isort, toml, yaml, pyupgrade, docformatter, and flake8\n- Migrate to GitHub Actions\n\n## 1.0.0\n\n- Updated documentation on [Readthedocs](https://generic.readthedocs.io)\n- Fix `multimethod.otherwise` clause\n\n## 1.0.0b1\n\n- Ported the code to Python 3.7, Python 2 is no longer supported\n- Multimethods now have their own module\n- The interface now mimics `functools.singledispatch`:\n  - the `when` method has been renamed to `register`\n  - overriding of methods is no longer possible\n\n## 0.3.1\n\n- Minor fixes in distribution.\n\n## 0.3\n\n- Event management with event inheritance support.\n\n## 0.2\n\n- Methods with multidispatch by object type and positional arguments.\n- Override multifunctions with ``override`` method.\n\n## 0.1\n\n- Registry with simple and type axes.\n- Functions with multidispatch by positional arguments.\n',
    'author': 'Andrey Popp',
    'author_email': '8mayday@gmail.com',
    'maintainer': 'Arjan Molenaar',
    'maintainer_email': 'gaphor@gmail.com',
    'url': 'https://generic.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
