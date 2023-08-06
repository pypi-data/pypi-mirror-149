# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['visvasc']

package_data = \
{'': ['*']}

install_requires = \
['dash>=2.3.1,<3.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'plotly>=5.7.0,<6.0.0']

setup_kwargs = {
    'name': 'visvasc',
    'version': '0.1.0',
    'description': 'A visualation tool for vasculature pressure and flow.',
    'long_description': '# VisVasc\n\nA simple visualisation tool for 1D networks. \n\n- [ ] Add a short intro/gif.\n\n## Installation\n\n- [ ] Add installation instructions.\n\n## Examples\n\nFor examples see the `examples/` directory.\n\n- [ ] Have some examples in the README.\n\n## Contributing\n\n- For contributing guidelines see [CONTRIBUTING](CONTRIBUTING.md).\n\n## Documentation\n\n- [ ] Genrate API documentation.\n',
    'author': 'Alex',
    'author_email': 'adrysdale@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/abdrysdale/vis-vasc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
