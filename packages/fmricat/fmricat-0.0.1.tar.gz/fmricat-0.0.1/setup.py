# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fmricat']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.1.3,<9.0.0',
 'nilearn>=0.9.1,<0.10.0',
 'nipype>=1.6.9,<2.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pybids>=0.15.1,<0.16.0',
 'rich>=12.4.0,<13.0.0',
 'scipy==1.8.0',
 'sklearn>=0.0,<0.1',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['denoiser = fmricat.denoiser:main()']}

setup_kwargs = {
    'name': 'fmricat',
    'version': '0.0.1',
    'description': 'An automated fMRI analysis toolbox',
    'long_description': None,
    'author': 'seven',
    'author_email': 'yusaiwen@mail.bnu.edu.cn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.10.2',
}


setup(**setup_kwargs)
