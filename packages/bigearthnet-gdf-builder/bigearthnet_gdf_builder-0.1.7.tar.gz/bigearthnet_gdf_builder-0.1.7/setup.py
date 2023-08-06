# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigearthnet_gdf_builder']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4,<2.0',
 'bigearthnet-common>=2.4,<=3.0',
 'fastcore>=1.3,<2.0',
 'geopandas>=0.10,<0.11',
 'natsort>=8,<9',
 'pyarrow>=6,<7',
 'pydantic>=1.8,<2.0',
 'pygeos>=0.12,<0.13',
 'rich>=10',
 'typer>=0.4,<0.5']

entry_points = \
{'console_scripts': ['ben_gdf_builder = '
                     'bigearthnet_gdf_builder.builder:_run_gdf_cli']}

setup_kwargs = {
    'name': 'bigearthnet-gdf-builder',
    'version': '0.1.7',
    'description': 'A package to generate and extend BigEarthNet GeoDataFrames.',
    'long_description': "# BigEarthNet GDF Builder\n[![Tests](https://img.shields.io/github/workflow/status/kai-tub/bigearthnet_gdf_builder/CI?color=dark-green&label=%20Tests)](https://github.com/kai-tub/bigearthnet_gdf_builder/actions/workflows/main.yml)\n[![License](https://img.shields.io/pypi/l/bigearthnet_gdf_builder?color=dark-green)](https://github.com/kai-tub/bigearthnet_gdf_builder/blob/main/LICENSE)\n[![PyPI version](https://badge.fury.io/py/bigearthnet-gdf-builder.svg)](https://pypi.org/project/bigearthnet-gdf-builder/)\n[![Auto Release](https://img.shields.io/badge/release-auto.svg?colorA=888888&colorB=9B065A&label=auto&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAACzElEQVR4AYXBW2iVBQAA4O+/nLlLO9NM7JSXasko2ASZMaKyhRKEDH2ohxHVWy6EiIiiLOgiZG9CtdgG0VNQoJEXRogVgZYylI1skiKVITPTTtnv3M7+v8UvnG3M+r7APLIRxStn69qzqeBBrMYyBDiL4SD0VeFmRwtrkrI5IjP0F7rjzrSjvbTqwubiLZffySrhRrSghBJa8EBYY0NyLJt8bDBOtzbEY72TldQ1kRm6otana8JK3/kzN/3V/NBPU6HsNnNlZAz/ukOalb0RBJKeQnykd7LiX5Fp/YXuQlfUuhXbg8Di5GL9jbXFq/tLa86PpxPhAPrwCYaiorS8L/uuPJh1hZFbcR8mewrx0d7JShr3F7pNW4vX0GRakKWVk7taDq7uPvFWw8YkMcPVb+vfvfRZ1i7zqFwjtmFouL72y6C/0L0Ie3GvaQXRyYVB3YZNE32/+A/D9bVLcRB3yw3hkRCdaDUtFl6Ykr20aaLvKoqIXUdbMj6GFzAmdxfWx9iIRrkDr1f27cFONGMUo/gRI/jNbIMYxJOoR1cY0OGaVPb5z9mlKbyJP/EsdmIXvsFmM7Ql42nEblX3xI1BbYbTkXCqRnxUbgzPo4T7sQBNeBG7zbAiDI8nWfZDhQWYCG4PFr+HMBQ6l5VPJybeRyJXwsdYJ/cRnlJV0yB4ZlUYtFQIkMZnst8fRrPcKezHCblz2IInMIkPzbbyb9mW42nWInc2xmE0y61AJ06oGsXL5rcOK1UdCbEXiVwNXsEy/6+EbaiVG8eeEAfxvaoSBnCH61uOD7BS1Ul8ESHBKWxCrdyd6EYNKihgEVrwOAbQruoytuBYIFfAc3gVN6iawhjKyNCEpYhVJXgbOzARyaU4hCtYizq5EI1YgiUoIlT1B7ZjByqmRWYbwtdYjoWoN7+LOIQefIqKawLzK6ID69GGpQgwhhEcwGGUzfEPAiPqsCXadFsAAAAASUVORK5CYII=)](https://github.com/intuit/auto)\n<!-- [![Conda Version](https://img.shields.io/conda/vn/conda-forge/bigearthnet-gdf-builder?color=dark-green)](https://anaconda.org/conda-forge/bigearthnet-gdf-builder) -->\n\n> A package to generate and extend BigEarthNet GeoDataFrame's.\n\nThis library provides a collection of functions to generate and extend GeoDataFrames for the [BigEarthNet](https://bigearth.net) dataset.\n\n`bigearthnet_gdf_builder` tries to accomplish two goals:\n\n1. Easily generate [geopandas](https://geopandas.org/en/stable/) [GeoDataFrame](https://geopandas.org/en/stable/getting_started/introduction.html)'s by passing a BigEarthNet archive directory.\n   - Allow for easy top-level statistical analysis of the data in a familiar _pandas_-style\n   - Provide functions to enrich GeoDataFrames with often required BigEarthNet metadata (like the season or country of the patch)\n2. Simplify the building procedure by providing a command-line interface with reproducible results\n\nOne of the primary purposes of the dataset is to allow deep learning researchers and practitioners to train their models on the _recommended_ BigEarthNet satellite data.\nIn that regard, there is a general recommendation to drop patches that are covered by seasonal snow or clouds/shadows.\nAlso, the novel 19-class nomenclature should be preferred over the original 43-class nomenclature.\nAs a result of these recommendations, some patches have to be _excluded_ from the original raw BigEarthNet dataset that is provided at [BigEarthNet](https://bigearth.net).\n\nTo simplify the procedure of pre-converting the JSON metadata files, the library provides a single command that will generate a recommended GeoDataFrame with extra metadata (country/season data of each patch) while dropping all patches that are not recommended for deep learning research.\nFunctions for both archives, BEN-S1 and BEN-S2, are provided.\n",
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
