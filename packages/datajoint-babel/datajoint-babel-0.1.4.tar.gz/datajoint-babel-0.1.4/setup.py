# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datajoint_babel', 'datajoint_babel.model']

package_data = \
{'': ['*']}

install_requires = \
['datajoint>=0.13.4,<0.14.0', 'parse>=1.19.0,<2.0.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'datajoint-babel',
    'version': '0.1.4',
    'description': 'Generate schema code from model definitions for both Python and MATLAB',
    'long_description': '![PyPI](https://img.shields.io/pypi/v/datajoint-babel)\n![PyPI - Status](https://img.shields.io/pypi/status/datajoint-babel)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/datajoint-babel)\n\n# datajoint-babel\nGenerate schema code from model definitions for both Python and MATLAB (and eventually vice versa).\n\nSay you\'re a lab that uses both Python and MATLAB, this lets you declare your models once and then generate\nboth Python and MATLAB versions of them, rather than having two potentially mutually contradictory sets of\nmodels. Keep explicit structure and avoid implicit model recreation from the database <3.\n\nMore generally a pythonic adapter interface from an explicit data model (thanks [pydantic](https://pydantic-docs.helpmanual.io/)!) to datajoint models so other tools can \npatch in more easily!\n\nSo far just a single afternoon project, but will be the means by which autopilot interfaces directly with datajoint :)\n\n# Example\n\n## Source a model from a string\n\n```python\n>>> from datajoint_babel.model import Table\n>>> from pprint import pprint\n>>> tab = Table.from_definition(name=\'User\', tier=\'Manual\', definition="""\n    # database users\n    username : varchar(20)   # unique user name\n    ---\n    first_name : varchar(30)\n    last_name  : varchar(30)\n    role : enum(\'admin\', \'contributor\', \'viewer\')\n    """\n)\n>>> tab.dict()\n{\'name\': \'User\',\n \'tier\': \'Manual\',\n \'comment\': {\'comment\': \'database users\'},\n \'keys\': [{\'name\': \'username\',\n   \'datatype\': {\'datatype\': \'varchar\', \'args\': 20, \'unsigned\': False},\n   \'comment\': \'unique user name\',\n   \'default\': None}],\n \'attributes\': [{\'name\': \'first_name\',\n   \'datatype\': {\'datatype\': \'varchar\', \'args\': 30, \'unsigned\': False},\n   \'comment\': \'\',\n   \'default\': None},\n  {\'name\': \'last_name\',\n   \'datatype\': {\'datatype\': \'varchar\', \'args\': 30, \'unsigned\': False},\n   \'comment\': \'\',\n   \'default\': None},\n  {\'name\': \'role\',\n   \'datatype\': {\'datatype\': \'enum\',\n    \'args\': ["\'admin\'", " \'contributor\'", " \'viewer\'"],\n    \'unsigned\': False},\n   \'comment\': \'\',\n   \'default\': None}]}\n\n>>> pprint(tab.__dict__)\n{\'attributes\': [Attribute(name=\'first_name\', datatype=DJ_Type(datatype=\'varchar\', args=30, unsigned=False), comment=\'\', default=None),\n                Attribute(name=\'last_name\', datatype=DJ_Type(datatype=\'varchar\', args=30, unsigned=False), comment=\'\', default=None),\n                Attribute(name=\'role\', datatype=DJ_Type(datatype=\'enum\', args=["\'admin\'", " \'contributor\'", " \'viewer\'"], unsigned=False), comment=\'\', default=None)],\n \'comment\': Comment(comment=\'database users\'),\n \'keys\': [Attribute(name=\'username\', datatype=DJ_Type(datatype=\'varchar\', args=20, unsigned=False), comment=\'unique user name\', default=None)],\n \'name\': \'User\',\n \'tier\': \'Manual\'}\n```\n\n## Export to python...\n\n```python\n>>> print(tab.make(lang=\'python\'))\n\n@schema\nclass User(dj.Manual):\n    definition = """\n    # database users\n    username : varchar(20) # unique user name\n    ---\n    first_name : varchar(30)\n    last_name : varchar(30)\n    role : enum(\'admin\', \'contributor\', \'viewer\')\n```\n\n## And to MATLAB\n\n```python\n>>> print(tab.make(lang=\'matlab\'))\n\n%{\n# # database users\n# username : varchar(20) # unique user name\n---\n# first_name : varchar(30)\n# last_name : varchar(30)\n# role : enum(\'admin\', \'contributor\', \'viewer\')\n%}\nclassdef User < dj.Manual\nend\n```\n\n',
    'author': 'sneakers-the-rat',
    'author_email': 'JLSaunders987@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/auto-pi-lot/datajoint-babel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
