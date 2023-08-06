# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['my_mltools']

package_data = \
{'': ['*']}

install_requires = \
['kneed>=0.7.0,<0.8.0',
 'pandas>=1.4.2,<2.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'yellowbrick>=1.4,<2.0']

setup_kwargs = {
    'name': 'my-mltools',
    'version': '0.3.0',
    'description': 'My machine learning toolkit.',
    'long_description': '# my_mltools\n\n[![codecov](https://codecov.io/gh/YangWu1227/my_mltools/branch/main/graph/badge.svg?token=9ZL267TMVD)](https://codecov.io/gh/YangWu1227/my_mltools)\n\nMy machine learning toolkit.\n\n## Installation\n\n```bash\n$ pip install my_mltools\n```\n## License\n\n`my_mltools` was created by Yang Wu. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`my_mltools` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Yang Wu',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
