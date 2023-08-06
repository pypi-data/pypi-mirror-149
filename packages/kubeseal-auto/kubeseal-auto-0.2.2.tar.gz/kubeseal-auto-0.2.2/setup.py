# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kubeseal_auto']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.1.2,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'icecream>=2.1.2,<3.0.0',
 'kubernetes>=23.3.0,<24.0.0',
 'questionary>=1.10.0,<2.0.0']

entry_points = \
{'console_scripts': ['kubeseal-auto = kubeseal_auto.cli:cli']}

setup_kwargs = {
    'name': 'kubeseal-auto',
    'version': '0.2.2',
    'description': 'An interactive wrapper for kubeseal binary',
    'long_description': '# kubeseal-auto\n\nThe script is an interactive wrapper for kubeseal binary used to encrypt secrets for [sealed-secrets](https://github.com/bitnami-labs/sealed-secrets).\n\n[![asciicast](https://asciinema.org/a/ynpQetDq5gPnKgNhAo5oYH6hK.svg)](https://asciinema.org/a/ynpQetDq5gPnKgNhAo5oYH6hK)\n\n## Installation\nHomebrew can be used to install the script with all dependencies:\n```bash\npip install kubeseal-auto\n```\n\n## Usage\n\nTo run the script in fully interactive mode:\n```bash\nkubeseal-auto\n```\n\nTo select kubeconfig context:\n```bash\nkubeseal-auto --select\n```\n\nTo append or change key values in existing secret:\n```bash\nkubeseal-auto --edit secret-name.yaml\n```\n\nAdditionally, a "detached" mode is supported:\n```bash\n# Download sealed-secrets certificate for local signing\nkubeseal-auto --fetch\n# Generate SealedSecret with local certificate\nkubeseal-auto --cert <kubectl-context>-kubeseal-cert.crt\n```\n',
    'author': 'Vadim Gedz',
    'author_email': 'vadims@linux-tech.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shini4i/kubeseal-auto',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
