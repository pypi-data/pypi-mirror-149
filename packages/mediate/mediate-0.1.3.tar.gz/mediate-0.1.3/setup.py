# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mediate']

package_data = \
{'': ['*']}

install_requires = \
['registrate>=0.1.6,<0.2.0']

setup_kwargs = {
    'name': 'mediate',
    'version': '0.1.3',
    'description': 'Middleware for every occasion',
    'long_description': "# mediate\nMiddleware for every occasion\n\n## Installation\n```console\npip install mediate\n```\n\n## Usage\n```python\nimport mediate\n\nmiddleware = mediate.Middleware()\n\n@middleware\ndef shout(call_next, name):\n    return call_next(name.upper())\n\n@middleware\ndef exclaim(call_next, name):\n    return call_next(name + '!')\n\n@middleware.bind\ndef hello(name):\n    print(f'Hello, {name}')\n```\n\n```python\n>>> hello('sam')\nHello, SAM!\n>>>\n>>> middleware.remove(shout)\n>>> hello('sam')\nHello, sam!\n```\n",
    'author': 'Tom Bulled',
    'author_email': '26026015+tombulled@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tombulled/middleware',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
