# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schemainspect', 'schemainspect.graphlib', 'schemainspect.pg']

package_data = \
{'': ['*'], 'schemainspect.pg': ['sql/*']}

install_requires = \
['six', 'sqlalchemy']

entry_points = \
{'console_scripts': ['schemainspect = schemainspect:do_command']}

setup_kwargs = {
    'name': 'schemainspect',
    'version': '3.1.1651839513',
    'description': 'Schema inspection for PostgreSQL (and possibly others)',
    'long_description': '# `schemainspect`: SQL Schema Inspection\n\nSchema inspection for PostgreSQL (and potentially others in the future).\n\nInspects tables, views, materialized views, constraints, indexes, sequences, enums, functions, and extensions. Handles table partitioning and inheritance.\n\n**Limitations:** Function inspection only confirmed to work with SQL/PLPGSQL languages so far.\n\n## Basic Usage\n\nGet an inspection object from an already opened SQLAlchemy session or connection as follows:\n\n    from schemainspect import get_inspector\n    from sqlbag import S\n\n    with S(\'postgresql:///example\') as s:\n        i = get_inspector(s)\n\nThe inspection object has attributes for tables, views, and all the other things it tracks. At each of these attributes you\'ll find a dictionary (OrderedDict) mapping from fully-qualified-and-quoted-name-of-thing-in-database to information object.\n\nFor instance, the information about a table *books* would be accessed as follows:\n\n    >>> books_table = i.tables[\'"public"."books"\']\n    >>> books_table.name\n    \'books\'\n    >>> books_table.schema\n    \'public\'\n    >>> [each.name for each in books_table.columns]\n    [\'id\', \'title\', \'isbn\']\n\n\n## Documentation\n\nDocumentation is a bit patchy at the moment. Watch this space!\n\n\n## Author Credits\n\nInitial development, maintenance:\n\n- [djrobstep](https://github.com/djrobstep)\n\nContributions:\n\n- [BenSjoberg](https://github.com/BenSjoberg)\n- [johto](https://github.com/johto)\n\n\n## Install\n\nInstall with [pip](https://pip.pypa.io):\n\n    $ pip install schemainspect\n\nTo install psycopg2 (the PostgreSQL driver) at the same time as well:\n\n    $ pip install schemainspect[pg]\n',
    'author': 'Robert Lechte',
    'author_email': 'robertlechte@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/djrobstep/schemainspect',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
