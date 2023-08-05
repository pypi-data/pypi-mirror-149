# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipeline_views']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2', 'asgiref>=3.5.0', 'djangorestframework>=3.12.0']

extras_require = \
{'schema': ['uritemplate>=4.1.1', 'PyYAML>=6.0'],
 'typing': ['typing-extensions>=4.0'],
 'uvloop': ['uvloop>=0.16.0']}

setup_kwargs = {
    'name': 'drf-pipeline-views',
    'version': '0.6.2',
    'description': 'Django REST framework views using the pipeline pattern.',
    'long_description': '# Django REST Framework Pipeline Views\n\n[![Coverage Status][coverage-badge]][coverage]\n[![Workflow Status][status-badge]][status]\n[![PyPI][pypi-badge]][pypi]\n[![Licence][licence-badge]][licence]\n[![Last Commit][commit-badge]][repo]\n[![Issues][issues-badge]][issues]\n\n[![Python Version][version-badge]][pypi]\n[![Django Version][django-badge]][pypi]\n[![DRF Version][drf-badge]][pypi]\n\n```shell\npip install drf-pipeline-views\n```\n\n---\n\n**Documentation**: [https://mrthearman.github.io/drf-pipeline-views/](https://mrthearman.github.io/drf-pipeline-views/)\n\n**Source Code**: [https://github.com/MrThearMan/drf-pipeline-views/](https://github.com/MrThearMan/drf-pipeline-views/)\n\n---\n\nInspired by a talk on [The Clean Architecture in Python][clean] by Brandon Rhodes,\n**drf-pipeline-views** aims to simplify writing testable API endpoints with\n[Django REST framework][drf] using the *[Pipeline Design Pattern][pipeline]*.\n\nThe main idea behind the pipeline pattern is to process data in steps. Input from the previous step\nis passed to the next, resulting in a collection of "data-in, data-out" -functions. These functions\ncan be easily unit tested, since none of the functions depend on the state of the objects in the other parts\nof the pipeline. Furthermore, IO can be separated into its own step, making the other parts of the\nlogic simpler and faster to test by not having to mock or do any other special setup around the IO.\nThis also means that the IO block, or in fact any other part of the application, can be replaced as long as the\ndata flowing through the pipeline remains the same.\n\n```python\nfrom pipeline_views import BasePipelineView\n\nfrom .my_serializers import InputSerializer, OutputSerializer\nfrom .my_validators import validator\nfrom .my_services import io_func, logging_func, integration_func\n\n\nclass SomeView(BasePipelineView):\n    pipelines = {\n        "GET": [\n            InputSerializer,\n            validator,\n            io_func,\n            integration_func,\n            logging_func,\n            OutputSerializer,\n        ],\n    }\n```\n\n> **New in 0.6.0**, mixin classes were removed, BasePiplineView adds\n> view methods automatically based on pipeline definitions!\n\nHave a look at the [quickstart][quickstart] section in the documentation on basic usage.\n\n[clean]: https://archive.org/details/pyvideo_2840___The_Clean_Architecture_in_Python\n[drf]: https://www.django-rest-framework.org/\n[pipeline]: https://java-design-patterns.com/patterns/pipeline/\n[quickstart]: https://mrthearman.github.io/drf-pipeline-views/quickstart\n\n[coverage-badge]: https://coveralls.io/repos/github/MrThearMan/drf-pipeline-views/badge.svg?branch=main\n[status-badge]: https://img.shields.io/github/workflow/status/MrThearMan/drf-pipeline-views/Tests\n[pypi-badge]: https://img.shields.io/pypi/v/drf-pipeline-views\n[licence-badge]: https://img.shields.io/github/license/MrThearMan/drf-pipeline-views\n[commit-badge]: https://img.shields.io/github/last-commit/MrThearMan/drf-pipeline-views\n[issues-badge]: https://img.shields.io/github/issues-raw/MrThearMan/drf-pipeline-views\n[version-badge]: https://img.shields.io/pypi/pyversions/drf-pipeline-views\n[django-badge]: https://img.shields.io/pypi/djversions/drf-pipeline-views\n[drf-badge]: https://img.shields.io/badge/drf%20versions-3.12%20%7C%203.13-blue\n\n[coverage]: https://coveralls.io/github/MrThearMan/drf-pipeline-views?branch=main\n[status]: https://github.com/MrThearMan/drf-pipeline-views/actions/workflows/main.yml\n[pypi]: https://pypi.org/project/drf-pipeline-views\n[licence]: https://github.com/MrThearMan/drf-pipeline-views/blob/main/LICENSE\n[repo]: https://github.com/MrThearMan/drf-pipeline-views/commits/main\n[issues]: https://github.com/MrThearMan/drf-pipeline-views/issues',
    'author': 'Matti Lamppu',
    'author_email': 'lamppu.matti.akseli@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MrThearMan/drf-pipeline-views',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
