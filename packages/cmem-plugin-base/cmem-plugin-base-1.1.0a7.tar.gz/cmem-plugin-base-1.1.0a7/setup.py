# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmem_plugin_base',
 'cmem_plugin_base.dataintegration',
 'cmem_plugin_base.dataintegration.parameter']

package_data = \
{'': ['*']}

install_requires = \
['cmem-cmempy>=21.11.5,<22.0.0']

setup_kwargs = {
    'name': 'cmem-plugin-base',
    'version': '1.1.0a7',
    'description': 'Base classes for developing eccenca Coporate Memory plugins.',
    'long_description': '# cmem-plugin-base\n\nPython base classes for developing eccenca Coporate Memory plugins.\n\nIn order to kick-start developing eccenca Corporate Memory Plugins, please check out this project template: https://github.com/eccenca/cmem-plugin-template\n\n',
    'author': 'eccenca',
    'author_email': 'cmempy-developer@eccenca.com',
    'maintainer': 'Sebastian Tramp',
    'maintainer_email': 'sebastian.tramp@eccenca.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
