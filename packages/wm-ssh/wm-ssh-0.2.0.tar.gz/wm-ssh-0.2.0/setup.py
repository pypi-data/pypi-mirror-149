# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wm_ssh']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['wm-ssh = wm_ssh.cli:wm_ssh']}

setup_kwargs = {
    'name': 'wm-ssh',
    'version': '0.2.0',
    'description': 'Wikimedia ssh wrapper to expand host names',
    'long_description': '# wm-ssh\n\nSsh wrapper to expand wikimedia hostnames.\n\nCurrently it will try several sources, heavily using caches:\n* Known working entries\n* Netbox (https://netbox.wikimedia.org)\n* Openstack Browser (https://openstack-browser.toolforge.org)\n\nNOTE: The netbox feature needs you to have a token for netbox.wikimedia.org, see:\n    https://netbox.wikimedia.org/user/api-tokens/\n\n\n# Installation\n## pip\n\nJust `pip install wm-ssh`, that should bring in a new binary, wm-ssh.\n\n## Running from code\n\nNote that this mode will require some tweaks in the auto-completing for it to work.\n\nClone the code:\n```\ngit clone git@github.com:david-caro/wm-ssh.git\n```\n\nInstall dependencies with poetry:\n```\npoetry install\n```\n\nRun with poetry:\n```\npoetry run wm-ssh <MYHOST>\n```\n\n\n# Bash completion\n\nYou can use the wm-ssh.complete file (source it from your bashrc for example) to achieve bash completion features,\nthough they only work with wmcs openstack instances and known hosts.\n\n',
    'author': 'David Caro',
    'author_email': 'me@dcaro.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/david-caro/wm-ssh',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
