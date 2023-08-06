# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautobot_ssot',
 'nautobot_ssot.api',
 'nautobot_ssot.jobs',
 'nautobot_ssot.migrations',
 'nautobot_ssot.templatetags',
 'nautobot_ssot.tests']

package_data = \
{'': ['*'],
 'nautobot_ssot': ['templates/nautobot_ssot/*',
                   'templates/nautobot_ssot/templatetags/*']}

install_requires = \
['Markdown!=3.3.5', 'diffsync>=1.3.0,<2.0.0', 'nautobot>=1.0.3,<2.0.0']

entry_points = \
{'nautobot_ssot.data_sources': ['example = '
                                'nautobot_ssot.sync.example:ExampleSyncWorker'],
 'nautobot_ssot.data_targets': ['example = '
                                'nautobot_ssot.sync.example:ExampleSyncWorker']}

setup_kwargs = {
    'name': 'nautobot-ssot',
    'version': '1.1.1',
    'description': 'Nautobot Single Source of Truth',
    'long_description': '# Nautobot Single Source of Truth (SSoT)\n\nA plugin for [Nautobot](https://github.com/nautobot/nautobot). This plugin facilitates integration and data synchronization between various "source of truth" (SoT) systems, with Nautobot acting as a central clearinghouse for data - a Single Source of Truth, if you will.\n\nA goal of this plugin is to make it relatively quick and straightforward to [develop and integrate](https://nautobot-plugin-ssot.readthedocs.io/en/latest/developing_jobs/) your own system-specific Data Sources and Data Targets into Nautobot with a common UI and user experience.\n\n## Installation\n\nThe plugin is available as a Python package in PyPI and can be installed with `pip`:\n\n```shell\npip install nautobot-ssot\n```\n\n> This plugin is compatible with Nautobot 1.0.3 and higher.\n\nOnce installed, the plugin needs to be enabled in your `nautobot_config.py`:\n\n```python\n# In your nautobot_config.py\nPLUGINS = ["nautobot_ssot"]\n\nPLUGINS_CONFIG = {\n    "nautobot_ssot": {\n        "hide_example_jobs": False,  # defaults to False if unspecified\n    }\n}\n```\n\nThe plugin behavior can be controlled with the following list of settings:\n\n- `"hide_example_jobs"`: By default this plugin includes a pair of example data source / data target jobs so that you can see how it works without installing any additional plugins to provide specific system integrations. Once you have installed or developed some "real" system integrations to work with this plugin, you may wish to hide the example jobs, which you may do by setting this configuration setting to `True`.\n\n## Usage\n\nRefer to the [documentation](https://nautobot-plugin-ssot.readthedocs.io/en/latest/) for usage details.\n\n## Questions\n\nFor any questions or comments, please check the [FAQ](FAQ.md) first and feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #networktocode).\nSign up [here](http://slack.networktocode.com/)\n\n## Screenshots\n\n![Dashboard screenshot](https://nautobot-plugin-ssot.readthedocs.io/en/latest/images/dashboard_initial.png)\n\n![Data Source detail view](https://nautobot-plugin-ssot.readthedocs.io/en/latest/images/data_source_detail.png)\n\n![Sync detail view](https://nautobot-plugin-ssot.readthedocs.io/en/latest/images/sync_detail.png)\n\n![Example data source - Arista CloudVision](https://nautobot-plugin-ssot.readthedocs.io/en/latest/images/example_cloudvision.png)\n\n![Example data target - ServiceNow](https://nautobot-plugin-ssot.readthedocs.io/en/latest/images/example_servicenow.png)\n',
    'author': 'Network to Code, LLC',
    'author_email': 'opensource@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nautobot/nautobot-plugin-ssot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
