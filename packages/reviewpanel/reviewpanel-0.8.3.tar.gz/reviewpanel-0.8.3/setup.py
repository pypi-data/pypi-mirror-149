# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reviewpanel', 'reviewpanel.migrations', 'reviewpanel.templatetags']

package_data = \
{'': ['*'],
 'reviewpanel': ['static/css/*',
                 'static/img/rp_icons/*',
                 'static/js/*',
                 'templates/admin/reviewpanel/*',
                 'templates/admin/reviewpanel/cohort/*',
                 'templates/reviewpanel/*']}

install_requires = \
['formative>=0.9.7']

extras_require = \
{':python_version >= "3.8" and python_version < "3.9"': ['backports.zoneinfo']}

entry_points = \
{'formative.plugin': ['reviewpanel = reviewpanel:FormativePluginMeta']}

setup_kwargs = {
    'name': 'reviewpanel',
    'version': '0.8.3',
    'description': 'Formative plugin for reviewing and scoring applicant submissions',
    'long_description': 'A [Formative](https://github.com/johncronan/formative) plugin for reviewing\nand scoring applicant submissions, **reviewpanel** allows a group of people to\nevaluate the submissions on a Formative form. You can create cohorts and\npresentation formats, set up panelist logins, define metrics, and\ndetermine scores.\n',
    'author': 'John Kyle Cronan',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/johncronan/reviewpanel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
