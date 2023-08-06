# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['userdefinedfields', 'userdefinedfields.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2.24']

setup_kwargs = {
    'name': 'django-user-defined-fields',
    'version': '0.0.17',
    'description': 'A Django app for user defined fields',
    'long_description': "# django-user-defined-fields\n\n[![PyPI version](https://badge.fury.io/py/django-user-defined-fields.svg)](https://badge.fury.io/py/django-user-defined-fields)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nDjango Used Defined Fields is a simple way to allow your users to add extra fields to your models, based on JSONField.\n\n\n## Installation\n\nStandard pip install:\n\n```bash\npip install django-user-defined-fields\n```\n\n\n## Quickstart\n\n```python\nfrom userdefinedfields.models import ExtraFieldsJSONField\n\n\nclass Example(models.Model):\n  extra_fields = ExtraFieldsJSONField()\n\n```\n\n## Tests\nRun tests in example directory with `python manage.py test library`\n\n\n# Settings\n```\nUSERDEFINEDFIELDS_INPUT_CLASSES = 'd-none'  # hide the textarea if you're using a frontend solution\n```\n",
    'author': 'Aidan Lister',
    'author_email': 'aidan@uptickhq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uptick/django-user-defined-fields/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
