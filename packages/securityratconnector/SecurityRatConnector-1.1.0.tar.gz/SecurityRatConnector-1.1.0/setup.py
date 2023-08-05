# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['securityratconnector']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'securityratconnector',
    'version': '1.1.0',
    'description': 'An API connector for SecurityRat',
    'long_description': '# SecurityRatConnector\nAn API connector for [SecurityRat](https://github.com/SecurityRAT/SecurityRAT) written in python\n\n## Requirements\n- Python >= 3.6\n- Requests\n\n## Installation\nInstall with pip\n\n````\npip install securityratconnector\n````\n\n## Documentation\nhttps://dcfsec.github.io/SecurityRatConnector/\n\n## Versioning\n\nWe use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/dcfSec/SecurityRatConnector/tags). \n\n## Authors\n\n * [dcfSec](https://github.com/dcfSec) - *Initial work*\n\nSee also the list of [contributors](https://github.com/dcfSec/SecurityRatConnector/contributors) who participated in this project.\n\n## License\n\nThis project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details',
    'author': 'dcfSec',
    'author_email': 'contributor@dcfsec.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dcfSec/SecurityRatConnector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
