# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsd_job_bot']

package_data = \
{'': ['*']}

install_requires = \
['jira>=3.2.0,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'texttable>=1.6.4,<2.0.0']

entry_points = \
{'console_scripts': ['jsd_job_bot = jsd_job_bot:main']}

setup_kwargs = {
    'name': 'jsd-job-bot',
    'version': '0.0.3',
    'description': 'Jira Service Desk job tracker.',
    'long_description': "# jsd_job_bot\n\nShows which jobs are in my JSD queue\n\nInstallation: `pip install jsd-job-bot`\n\nYou need a `jsd_job_bot.ini` config file:\n\n    [DEFAULT]\n    JSD_API_KEY=<your api key>\n    JSD_HOSTNAME=<your instance>.atlassian.net\n    JSD_USERNAME=<your email address>\n\nYou can also set `SHOW_ALL_JOBS` which will show everything regardless of status.\n\nThe config file needs to be in one of these places:\n\n* The current working directory.\n* `~/.config`\n* `~/etc/`\n\nRun it, it'll show you what you've got assigned to you.\n",
    'author': 'James Hodgkinson',
    'author_email': 'james@terminaloutcomes.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yaleman/jsd_job_bot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
