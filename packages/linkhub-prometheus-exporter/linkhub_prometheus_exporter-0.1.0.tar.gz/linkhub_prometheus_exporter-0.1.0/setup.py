# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['linkhub_prometheus_exporter']

package_data = \
{'': ['*']}

install_requires = \
['dynaconf>=3.1.8,<4.0.0',
 'prometheus-client>=0.14.1,<0.15.0',
 'requests>=2.27.1,<3.0.0',
 'types-requests>=2.27.25,<3.0.0']

entry_points = \
{'console_scripts': ['exporter = linkhub_prometheus_exporter.exporter:main']}

setup_kwargs = {
    'name': 'linkhub-prometheus-exporter',
    'version': '0.1.0',
    'description': 'A Prometheus metrics exporter for Alcatel Linkhub 4G router boxes',
    'long_description': 'None',
    'author': 'Gergely Imreh',
    'author_email': 'gergely@imreh.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
