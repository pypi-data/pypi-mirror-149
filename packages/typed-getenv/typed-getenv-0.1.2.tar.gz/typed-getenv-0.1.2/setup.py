# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typed_getenv']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'typed-getenv',
    'version': '0.1.2',
    'description': 'A simple module for environment variable based configuration',
    'long_description': '# Typed getenv\n\nA simple package for minimalistic environment-based configurations. No dependencies required.\n\n---\n\n## What this module is for\n\nAs microservices become more and more popular there\'s a need for environment based configuration.\n\n**Why not use a config ini/YAML/JSON/etc. file?** Microservices are mostly run in containers. Sometimes you might not\nhave access to the host environment to build containers yourself with filled config files embedded into them or mount\nfiles into the container. The most logical option then is to provide a prebuilt container image and a set of environment\nvariables that define it\'s behaviour.\n\n**Why not use standard `os.getev()`?** Getenv is mostly for storing strings, however configurations often need to\ninclude integers, floats and logical values. Getenv would require some very trivial custom logic to be rewritten over\nand over again to convert strings into the desired types of values and validate them. This library provides this code.\n\n**Why create a new package?** Indeed there are already solutions to the problems listed above.\n[environ-config](https://pypi.org/project/environ-config/) and [Pydantic](https://pypi.org/project/pydantic/) are nice\ntools that would be great for that job, but they\'re clearly an overkill for the task when you have a lightweight\nmicroservice application with only a few environment variables to parse. This package on the other hand has **no\ndependencies** and provides global access to the needed variables across all your application **no initialization and\nconfiguration required**.\n\n## Installation\n\nTo acquire the module head over to the terminal and install the module using your favourite package manager e.g.\n`pip instal typed_getenv` or `poetry add typed_getenv`.\n\n## Usage\n\nTyped getenv has a very simple interface that is pretty much just a wrapper over standard `os.getenv()` with a couple\nadditional arguments and some custom exceptions.\n\nThis example demonstrates the usage of the module.\n\n```python\nfrom typing import Optional\n\n# Import the getenv function from the package\nfrom typed_getenv import getenv\n\n# Get an optional string parameter\n# Variable name and the default value are positional (as in os.getenv()) but "var_type" and "optional"\n# arguments are strictly keyword. "var_type" defaults to Optional[str] and "optional" defaults to False.\nTEST_OPTIONAL_STR_VALUE: Optional[str] = getenv("TEST_OPTIONAL_STR_VALUE", optional=True)\n\n# Get a mandatory string parameter (if unset raises VariableUnsetError)\n# Note that although the default is set it will still raise an exception unless the "optional" argument is set to True\nTEST_STR_VALUE: str = getenv("TEST_STR_VALUE", default="foo", var_type=str)\n\n# Get an integer (can also be optional).\n# If type conversion is not possible - raises TypeMismatchError\nTEST_INT_VALUE: int = getenv("TEST_INT_VALUE", 42, var_type=int)\n\n# Get a float (can also be optional)\nTEST_FLOAT_VALUE: float = getenv("TEST_FLOAT_VALUE", 4.2, var_type=float)\n\n# Get a bool value\n# Strings "1", "yes", "true", "on" and "enable" will be interpreted as True\n# Strings "0", "no", "false", "off" and "disable" will be interpreted as False\n# Case doesn\'t matter. Other values will result in raise of UnprocessableValueError\nTEST_BOOL_VALUE: bool = getenv("TEST_BOOL_VALUE", False, var_type=bool)\n```\n\n## Contributing\n\nIf you want to contribute to the development - file an issue or create a pull request on the GitHub page for this\nmodule.\n',
    'author': 'arseniiarsenii',
    'author_email': 'arseniivelichko2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arseniiarsenii/typed-getenv/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
