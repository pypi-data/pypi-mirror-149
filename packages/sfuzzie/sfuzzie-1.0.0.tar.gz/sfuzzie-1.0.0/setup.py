# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sfuzzie']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sfuzzie',
    'version': '1.0.0',
    'description': 'simple fuzz functionality for python',
    'long_description': '\n# sfuzzie\nsfuzzie is a simple fuzz tree algorithem, provide fuzzing for words\n\n## example\n\n```py\nfrom sfuzzie import fuzz\n\nfuzzer = fuzz([\n    "hello world",\n    "fuzzing",\n    "fuling"\n])\n\nprint(fuzzer.suggest("hel fu w"))\n```\n\n### output:\n```\n[[\'hello\'], [\'fuzzing\', \'fuling\'], [\'world\']]\n```\n\n## install\n```\npython3 -m pip3 install sfuzzie\n```\n',
    'author': 'dsal3389',
    'author_email': 'dsal3389@foo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
