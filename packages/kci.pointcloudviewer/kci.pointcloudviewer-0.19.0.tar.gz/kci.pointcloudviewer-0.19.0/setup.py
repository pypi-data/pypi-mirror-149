# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kci',
 'kci.pointcloudviewer',
 'kci.pointcloudviewer._internal',
 'kci.pointcloudviewer._internal.members',
 'kci.pointcloudviewer._internal.protobuf',
 'kci.pointcloudviewer._vendor.pypcd']

package_data = \
{'': ['*'], 'kci.pointcloudviewer': ['public/*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0',
 'numpy>=1.20.2,<2.0.0',
 'protobuf>=3.15.6,<4.0.0',
 'python-lzf>=0.2.4,<0.3.0',
 'websockets>=8.1,<9.0']

setup_kwargs = {
    'name': 'kci.pointcloudviewer',
    'version': '0.19.0',
    'description': 'Webブラウザ上に点群を描画する python ライブラリ',
    'long_description': None,
    'author': 'Kurusugawa Computer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kurusugawa-computer/pointcloud-viewer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
