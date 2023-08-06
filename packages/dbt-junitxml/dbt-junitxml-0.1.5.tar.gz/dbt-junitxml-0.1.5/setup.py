# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dbt_junitxml']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1', 'junit-xml>=1.9']

entry_points = \
{'console_scripts': ['dbt-junitxml = dbt_junitxml.main:cli']}

setup_kwargs = {
    'name': 'dbt-junitxml',
    'version': '0.1.5',
    'description': '',
    'long_description': '# dbt-junitxml\n\nConvert your dbt test results into jUnit XML format so that CI/CD platforms (such as Jenkins, CircleCI, etc.)\ncan better report on tests in their UI.\n\n## Installation\n\n```shell\npip install dbt-junitxml\n```\n\n\n## Usage\n\nWhen you run your dbt test suite, the output is saved under `target/run_results.json`. Run the following command\nto parse your run results and output a jUnit XML formatted report named `report.xml`.\n\n```shell\ndbt-junitxml parse target/run_results.json report.xml\n```\n\n## Limitations\n\nCurrently, only v4 of the [Run Results](https://docs.getdbt.com/reference/artifacts/run-results-json) specifications is supported.\n',
    'author': 'Charles Lariviere',
    'author_email': 'charleslariviere1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chasleslr/dbt-junitxml',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
