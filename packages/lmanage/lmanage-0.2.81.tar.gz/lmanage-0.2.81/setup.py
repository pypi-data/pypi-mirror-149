# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lmanage',
 'lmanage.configurator',
 'lmanage.configurator.folder_configuration',
 'lmanage.configurator.user_attribute_configuration',
 'lmanage.configurator.user_group_configuration',
 'lmanage.configurator.utils',
 'lmanage.mapview',
 'lmanage.mapview.utils']

package_data = \
{'': ['*']}

install_requires = \
['autopep8>=1.6.0,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'coloredlogger>=1.3.12,<2.0.0',
 'coloredlogs>=15.0,<16.0',
 'debugpy>=1.3.0,<2.0.0',
 'flake8>=4.0.1,<5.0.0',
 'icecream>=2.1.0,<3.0.0',
 'ipython>=7.20.0,<8.0.0',
 'lkml>=1.1.1,<2.0.0',
 'lookml>=3.0.3,<4.0.0',
 'pandas>=1.2.2,<2.0.0',
 'pylint>=2.9.5,<3.0.0',
 'pynvim>=0.4.3,<0.5.0',
 'pytest-mock>=3.5.1,<4.0.0',
 'snoop>=0.3.0,<0.4.0',
 'sqlparse>=0.4.1,<0.5.0',
 'tabulate>=0.8.8,<0.9.0',
 'verboselogs>=1.7,<2.0']

entry_points = \
{'console_scripts': ['lmanage = lmanage.cli:lmanage']}

setup_kwargs = {
    'name': 'lmanage',
    'version': '0.2.81',
    'description': "LManage is a collection of useful tools for Looker admins to help curate and cleanup content and it's associated source LookML.",
    'long_description': "# Lmanage\n## What is it.\nLManage is a collection of useful tools for [Looker](https://looker.com/) admins to help curate and cleanup content and it's associated source [LookML](https://docs.looker.com/data-modeling/learning-lookml/what-is-lookml).\n\n## How do i Install it.\nLmanage can be found on [pypi](#).\n```\npip install lmanage\n```\n\n## How do I Use it.\n### Commands\nLManage will ultimately will have many different commands as development continues \n| Status  | Command    | Rationale                                                                                                                                                                                            |\n|---------|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n| Live    | [mapview](https://github.com/looker-open-source/lmanage/tree/main/instructions/mapview_README.md) | Find the LookML fields and tables that are associated with a piece of Looker content                          |\n| Live    | [configurator](https://github.com/looker-open-source/lmanage/tree/main/instructions/configurator_README.md)| Configure your Looker Instance Group, Folder, Role and User Attributes via a Yaml based Config File |\n| Planned | removeuser | Based on last time logged in, prune Looker users to ensure a performant, compliant Looker instance                                                                                                   |\n| Planned | dcontent   | Iterate through an input of content, delete content and back it up using [gzr](https://github.com/looker-open-source/gzr) for easy restoration                                                                                               |\n| Planned | bcontent   | Iterate through all broken content (using content validator) and email a customized message to each dashboard owner                                                                                  |\n| Planned | scoper     | Takes in a model file, elminates the * includes, iterate through the explores and joins and creates a fully scoped model include list for validation performance and best practice code organization |\n\n#### help and version\n```\nlmanage --help\nUsage: lmanage [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  mapview\n```\n#### mapview\nThe mapview command will find the etymology of the content on your dashboard, exporting a CSV that looks like [this](https://docs.google.com/spreadsheets/d/1TzeJW46ml0uzO9RdLOOLxwtvUWjhmZxoa-xq4pbznV0/edit?resourcekey=0-xbWC87hXYFNgy1As06NncA#gid=900312158).\n\n[instructions](https://github.com/looker-open-source/lmanage/tree/main/instructions/mapview_README.md)\n\n#### configurator\nThe configurator command will allow you to manage your Looker security and access settings from a simple text based Yaml file. This process can be version controlled and productionalized using a gitops workflow.\n\n[instructions](https://github.com/looker-open-source/lmanage/tree/main/instructions/configurator_README.md)\n\n\n**This is not an officially supported Google Product.**\n",
    'author': 'hselbie',
    'author_email': 'hselbie@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/looker-open-source/lmanage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
