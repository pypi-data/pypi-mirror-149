# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['migra']

package_data = \
{'': ['*']}

install_requires = \
['schemainspect>=3.1.1652015119', 'six', 'sqlbag']

extras_require = \
{'pg': ['psycopg2-binary']}

entry_points = \
{'console_scripts': ['migra = migra:do_command']}

setup_kwargs = {
    'name': 'migra',
    'version': '3.0.1652017683',
    'description': 'Like `diff` but for PostgreSQL schemas',
    'long_description': '# migra: Like diff but for Postgres schemas\n\n- ## compare schemas\n- ## autogenerate migration scripts\n- ## autosync your development database from your application models\n- ## make your schema changes testable, robust, and (mostly) automatic\n\n`migra` is a schema diff tool for PostgreSQL, written in Python. Use it in your python scripts, or from the command line like this:\n\n    $ migra postgresql:///a postgresql:///b\n    alter table "public"."products" add column newcolumn text;\n\n    alter table "public"."products" add constraint "x" CHECK ((price > (0)::numeric));\n\n`migra` magically figures out all the statements required to get from A to B.\n\nMost features of PostgreSQL are supported.\n\n**Migra supports PostgreSQL >= 9 only.** Known issues exist with earlier versions. More recent versions are more comprehensively tested. Development resources are limited, and feature support rather than backwards compatibility is prioritised.\n\n## THE DOCS\n\nDocumentation is at [databaseci.com/docs/migra](https://databaseci.com/docs/migra).\n\n## Folks, schemas are good\n\nSchema migrations are without doubt the most cumbersome and annoying part of working with SQL databases. So much so that some people think that schemas themselves are bad!\n\nBut schemas are actually good. Enforcing data consistency and structure is a good thing. It’s the migration tooling that is bad, because it’s harder to use than it should be. ``migra`` is an attempt to change that, and make migrations easy, safe, and reliable instead of something to dread.\n\n## Contributing\n\nContributing is easy. [Jump into the issues](https://github.com/djrobstep/migra/issues), find a feature or fix you\'d like to work on, and get involved. Or create a new issue and suggest something completely different. If you\'re unsure about any aspect of the process, just ask.\n\n## Credits\n\n- [djrobstep](https://github.com/djrobstep): initial development, maintenance\n- [alvarogzp](https://github.com/alvarogzp): privileges support\n- [seblucas](https://github.com/seblucas): docker improvements\n- [MOZGIII](https://github.com/MOZGIII): docker support\n- [mshahbazi](https://github.com/mshahbazi): misc fixes and enhancements\n',
    'author': 'Robert Lechte',
    'author_email': 'robertlechte@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://databaseci.com/docs/migra',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
