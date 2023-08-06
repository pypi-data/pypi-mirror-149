# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netplanner',
 'netplanner.interfaces',
 'netplanner.interfaces.l2',
 'netplanner.interfaces.l3',
 'netplanner.loader',
 'netplanner.providers',
 'netplanner.providers.networkd',
 'netplanner.providers.networkd.files',
 'netplanner.providers.networkd.templates',
 'netplanner.providers.networkd.templates.netdev_includes',
 'netplanner.providers.networkd.templates.network_includes',
 'netplanner.sriov',
 'netplanner.sriov.files']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.1,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'dacite>=1.6.0,<2.0.0',
 'fqdn>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['netplanner = netplanner.__main__:main']}

setup_kwargs = {
    'name': 'netplanner',
    'version': '0.12.0',
    'description': 'Mimir the Netplanner is the ground of all network wisdöm',
    'long_description': "# netplanner\n\n## Description\n\nNetplanner implements the top-down datacenter approach for IP and Network Interface Management.\nIt plans the network on the host by using `systemd-networkd` as the underlying network configuration provider.\n\nIt refuses to implement L2 capabilities such as DHCP.\n\nIt also implements interfaces which are needed for L3 capabilities such as `Veth` and `Dummy` interface types.\n\nIt is open to be extended with other providers which have a different text-based input.\n\n## Architecture\n\n![Netplanner Overview and Architecture](docs/netplanner-overview.png)\n\n## Licenses\n\nRunning Code Licenses\n\n* Python 3.x - today | [PSF LICENSE AGREEMENT FOR PYTHON](https://docs.python.org/3/license.html)\n* dacite | [MIT License](https://github.com/konradhalas/dacite/blob/master/LICENSE)\n* PyYaml | [MIT License](https://github.com/yaml/pyyaml/blob/master/LICENSE)\n* fqdn   | [MPL-2 License](https://github.com/ypcrts/fqdn/blob/develop/LICENSE)\n* Jinja2 | [BSD-3 License](https://github.com/pallets/jinja/blob/main/LICENSE.rst)\n\nBuilding Tool for Dynamic Linked CLI Binary\n\n* PyOxidizer | [MPL-2 License](https://github.com/indygreg/PyOxidizer/blob/main/LICENSE)\n\n## How to use it\n\n```console\n# This is a developer command --local ensures that ./ is set on the output.\n$ netplanner --local --config examples/worker-config-old.yaml --output /run/systemd/network --only-networkd configure\n\n$ netplanner --help\nusage: netplanner [-h] [--version] [--config CONFIG] [--debug] [--local] [--only-sriov] [--reload] [--only-networkd] [--output OUTPUT]\n                  {configure,apply,generate} ...\n\noptions:\n  -h, --help            show this help message and exit\n  --version             show program's version number and exit\n  --config CONFIG       Defines the path to the configuration file or directory.\n  --debug               Enables debug logging.\n  --local               This templates the configuration into a local directory\n  --only-sriov          This only runs sriov configuration on supported interfaces.\n  --reload              This reloads networkd and networkctl via systemd.\n  --only-networkd       This templates only networkd configuration files.\n  --output OUTPUT       The output directory to which the files will be written.\n\nsubcommands:\n  valid subcommands\n\n  {configure,apply,generate}\n                        sub-command help\n    configure           Configure Network Adapters flawlessly with the knowledge of the netplanner.\n    apply               Configure Network Adapters flawlessly with the knowledge of the netplanner.\n    generate            Configure Network Adapters flawlessly with the knowledge of the netplanner.\n```\n\n## Examples Directory\n\nInside the examples directory you can have a overview of different types of configurations.\n",
    'author': 'Marcel Fest',
    'author_email': 'marcel.fest@telekom.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
