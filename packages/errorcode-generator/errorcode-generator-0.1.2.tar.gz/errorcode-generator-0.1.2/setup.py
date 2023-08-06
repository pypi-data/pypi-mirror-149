# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['errorcode_generator']
install_requires = \
['jinja2>=2.11.2,<3.0.0', 'typing>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['errorcode-generator = errorcode_generator:cli']}

setup_kwargs = {
    'name': 'errorcode-generator',
    'version': '0.1.2',
    'description': '根据模板文件生成各种错误码文本格式',
    'long_description': None,
    'author': 'riag',
    'author_email': 'riag@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
