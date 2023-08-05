# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigearthnet_gdf_builder']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4,<2.0',
 'bigearthnet-common>=2,<3',
 'fastcore>=1.3,<2.0',
 'geopandas>=0.10,<0.11',
 'natsort>=8,<9',
 'pyarrow>=6,<7',
 'pydantic>=1.8,<2.0',
 'pygeos>=0.12,<0.13',
 'rich>=10,<13',
 'typer>=0.4,<0.5']

entry_points = \
{'console_scripts': ['ben_gdf_builder = '
                     'bigearthnet_gdf_builder.builder:_run_gdf_cli']}

setup_kwargs = {
    'name': 'bigearthnet-gdf-builder',
    'version': '0.1.6',
    'description': 'A package to generate and extend BigEarthNet GeoDataFrames.',
    'long_description': '# BigEarthNet GeoDataFrame Builder\n\nSee the main documentation.\n',
    'author': 'Kai Norman Clasen',
    'author_email': 'k.clasen@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai-tub/bigearthnet_gdf_builder/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
