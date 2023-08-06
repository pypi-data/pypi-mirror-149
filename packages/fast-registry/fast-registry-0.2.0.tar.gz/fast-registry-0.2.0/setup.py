# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_registry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fast-registry',
    'version': '0.2.0',
    'description': 'Everything you need to implement maintainable and easy to use registry patterns in your project.',
    'long_description': '# Fast Registry\n[![](https://img.shields.io/pypi/v/fast-registry.svg)](https://pypi.python.org/pypi/fast-registry/)\n[![](https://github.com/danialkeimasi/fast-registry/workflows/tests/badge.svg)](https://github.com/danialkeimasi/fast-registry/actions)\n[![](https://img.shields.io/github/license/danialkeimasi/fast-registry.svg)](https://github.com/danialkeimasi/fast-registry/blob/master/LICENSE)\n\nEverything you need to implement maintainable and easy to use registry patterns in your project.\n# Installation\n\n```sh\npip install fast-registry\n```\n\n# Register Classes\nRegister classes with the same interface, enforce the type check and enjoy the benefits of type hints:\n\n![python fast-registry class example](./images/class-registration-example.png)\n\n\n# Register Functions\nRegister functions and benefit from the function annotations validator (optional):\n```py\nfrom fast_registry import FastRegistry, FunctionAnnotationValidator\n\ndatabase_registry = FastRegistry(\n    validators=[\n        FunctionAnnotationValidator(annotations=[("name", str)]),\n    ]\n)\n\n@database_registry.register("sqlite")\ndef sqlite_database_connection(name: str):\n    return f"sqlite connection {name}"\n\n```\n\n# Create Custom Validators\nCreate your own validators to validate registered classes/functions if you need to. By Creating a subclass of `RegistryValidator`, you can create your own validators.\n\n# Examples\n- [Class - Simple Type Checking](./examples/class.py)\n- [Class - Custom Registration](./examples/class-with-custom-validator.py)\n- [Function - Simple](./examples/function.py)\n- [Function - With Type Annotation Validation](./examples/function-with-validator.py)',
    'author': 'Danial Keimasi',
    'author_email': 'danialkeimasi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danialkeimasi/python-fast-registry',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
