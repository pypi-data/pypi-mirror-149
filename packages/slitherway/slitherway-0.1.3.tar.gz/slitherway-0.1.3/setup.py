# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slitherway']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'slitherway',
    'version': '0.1.3',
    'description': 'Python wrapper for the Flyway CLI',
    'long_description': '# Slitherway\n\n[![PyPi version](https://badgen.net/pypi/v/slitherway/)](https://pypi.org/project/slitherway/)\n\nSlitherway is a lightweight python wrapper around the [Flyway](https://flywaydb.org/) CLI.  \nIt allows you to run migrations directly from your python applications and tests\n\nIn order to use, you must have the Flyway CLI installed on your machine!\n\n## Example\n\nUsing slitherway is simple\n\n```py\nfrom slitherway.commands import migrate\nfrom slitherway.models import FlywayCommandArgs\n\nargs = FlywayCommandArgs(\n    user=pg.POSTGRES_USER,\n    password=pg.POSTGRES_PASSWORD,\n    locations=["migrations"],\n    url=f"jdbc:postgresql://localhost:{pg.get_exposed_port(5432)}/{pg.POSTGRES_DB}",\n)\n\nmigrate(args)\n```\n',
    'author': 'Ryan Brink',
    'author_email': 'rbweb@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/unredundant/slitherway',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
