# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resotoclient']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.3.0,<3.0.0',
 'cryptography>=36.0.2,<37.0.0',
 'jsons>=1.6.1,<2.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'resotoclient',
    'version': '0.1.7',
    'description': 'Resoto Python client library',
    'long_description': '# resotoclient-python\nPython client for Resoto\n\n## Installation\n\n```bash\npip install resotoclient\n```\n\n## Usage\n\n```python\nfrom resotoclient import ResotoClient\n\nclient = ResotoClient(url="https://localhost:8900", psk="changeme")\ninstances_csv = client.cli_execute("search is(instance) | tail 5 | list --csv")\n\nfor instance in instances_csv:\n    print(instance)\n```\n\nFor more examples see the examples directory.',
    'author': 'Some Engineering Inc.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/someengineering/resotoclient-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
