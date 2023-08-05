# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sword_to_json']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=4.4.0,<5.0.0', 'pysword>=0.2.7,<0.3.0']

setup_kwargs = {
    'name': 'sword-to-json',
    'version': '1.4.7',
    'description': 'Generate JSON Files of Bible Translations from SWORD Modules',
    'long_description': '![CI](https://github.com/evnskc/sword-to-json/actions/workflows/ci.yml/badge.svg)\n![CD](https://github.com/evnskc/sword-to-json/actions/workflows/cd.yml/badge.svg?branch=main)\n\n## Generate JSON Files of Bible Translations from SWORD Modules\n\nThe [SWORD project provides modules](http://crosswire.org/sword/modules/ModDisp.jsp?modType=Bibles) freely for common\nBible translations in different languages.\n\nSample JSON format.\n\n```json\n [\n  {\n    "number": 1,\n    "name": "Genesis",\n    "abbreviation": "Gen",\n    "chapters": [\n      {\n        "number": 1,\n        "verses": [\n          {\n            "number": 1,\n            "text": "In the beginning God created the heavens and the earth."\n          }\n        ]\n      }\n    ]\n  }\n]\n```\n\n## Installation\n\n1. Using ```pip```\n\n```commandline\npip install sword-to-json\n```\n\n2. Using ```poetry```\n\n```commandline\npoetry add sword-to-json\n```\n\n## Usage\n\n```text\npython -m sword_to_json sword module [--output OUTPUT]\n```\n\n```commandline\npython -m sword_to_json /home/user/Downloads/KJV.zip KJV --output /home/user/Downlods/KJV.json\n```',
    'author': 'evans',
    'author_email': 'evans@fundi.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/evnskc/sword-to-json',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
