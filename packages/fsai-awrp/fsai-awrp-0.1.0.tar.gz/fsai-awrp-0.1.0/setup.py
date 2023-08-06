# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fsai_awrp']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'fsai-awrp',
    'version': '0.1.0',
    'description': 'Library that helps an application report progress to Argo Workflows.',
    'long_description': '# fsai-awrp\nLibrary that helps an application report progress to Argo Workflows.\n',
    'author': 'Michael Mohamed',
    'author_email': 'michael@foundationstack.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fsai-dev/fsai-awrp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
