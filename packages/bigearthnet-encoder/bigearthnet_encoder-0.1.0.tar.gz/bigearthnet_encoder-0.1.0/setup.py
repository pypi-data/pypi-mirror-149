# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigearthnet_encoder']

package_data = \
{'': ['*']}

install_requires = \
['bigearthnet-common>=2,<3',
 'bigearthnet-patch-interface>=0.1,<0.2',
 'fastcore>=1.3.27,<2.0.0',
 'lmdb>=1.3.0,<2.0.0',
 'numpy>=1.19,<2.0',
 'pandas>=1.3.5,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'rasterio>=1.2.10,<2.0.0',
 'rich>=10,<14']

entry_points = \
{'console_scripts': ['ben_encoder = bigearthnet_encoder.encoder:encoder_cli']}

setup_kwargs = {
    'name': 'bigearthnet-encoder',
    'version': '0.1.0',
    'description': 'A flexible BigEarthNet encoder that allows one to quickly convert BigEarthNet to a DL-optimization data format.',
    'long_description': '# BigEarthNet Encoder\n\n[![Tests](https://img.shields.io/github/workflow/status/kai-tub/bigearthnet_encoder/CI?color=dark-green&label=%20Tests)](https://github.com/kai-tub/bigearthnet_encoder/actions/workflows/main.yml)\n[![License](https://img.shields.io/pypi/l/bigearthnet_encoder?color=dark-green)](https://github.com/kai-tub/bigearthnet_encoder/blob/main/LICENSE)\n[![PyPI version](https://badge.fury.io/py/bigearthnet-encoder.svg)](https://pypi.org/project/bigearthnet-encoder/)\n[![Auto Release](https://img.shields.io/badge/release-auto.svg?colorA=888888&colorB=9B065A&label=auto&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAACzElEQVR4AYXBW2iVBQAA4O+/nLlLO9NM7JSXasko2ASZMaKyhRKEDH2ohxHVWy6EiIiiLOgiZG9CtdgG0VNQoJEXRogVgZYylI1skiKVITPTTtnv3M7+v8UvnG3M+r7APLIRxStn69qzqeBBrMYyBDiL4SD0VeFmRwtrkrI5IjP0F7rjzrSjvbTqwubiLZffySrhRrSghBJa8EBYY0NyLJt8bDBOtzbEY72TldQ1kRm6otana8JK3/kzN/3V/NBPU6HsNnNlZAz/ukOalb0RBJKeQnykd7LiX5Fp/YXuQlfUuhXbg8Di5GL9jbXFq/tLa86PpxPhAPrwCYaiorS8L/uuPJh1hZFbcR8mewrx0d7JShr3F7pNW4vX0GRakKWVk7taDq7uPvFWw8YkMcPVb+vfvfRZ1i7zqFwjtmFouL72y6C/0L0Ie3GvaQXRyYVB3YZNE32/+A/D9bVLcRB3yw3hkRCdaDUtFl6Ykr20aaLvKoqIXUdbMj6GFzAmdxfWx9iIRrkDr1f27cFONGMUo/gRI/jNbIMYxJOoR1cY0OGaVPb5z9mlKbyJP/EsdmIXvsFmM7Ql42nEblX3xI1BbYbTkXCqRnxUbgzPo4T7sQBNeBG7zbAiDI8nWfZDhQWYCG4PFr+HMBQ6l5VPJybeRyJXwsdYJ/cRnlJV0yB4ZlUYtFQIkMZnst8fRrPcKezHCblz2IInMIkPzbbyb9mW42nWInc2xmE0y61AJ06oGsXL5rcOK1UdCbEXiVwNXsEy/6+EbaiVG8eeEAfxvaoSBnCH61uOD7BS1Ul8ESHBKWxCrdyd6EYNKihgEVrwOAbQruoytuBYIFfAc3gVN6iawhjKyNCEpYhVJXgbOzARyaU4hCtYizq5EI1YgiUoIlT1B7ZjByqmRWYbwtdYjoWoN7+LOIQefIqKawLzK6ID69GGpQgwhhEcwGGUzfEPAiPqsCXadFsAAAAASUVORK5CYII=)](https://github.com/intuit/auto)\n<!-- [![Conda Version](https://img.shields.io/conda/vn/conda-forge/bigearthnet-encoder?color=dark-green)](https://anaconda.org/conda-forge/bigearthnet-encoder) -->\n\nThe goal of the BigEarthNet Encoder library is to quickly transform the original BigEarthNet archive to a deep-learning optimized format.\nThe long-term goal is to support multiple output formats.\n\nTo simplify the process of working with BigEarthNet, each patch is first converted to a [BigEarthNet-Patch-Interface](https://docs.kai-tub.tech/bigearthnet_patch_interface/).\nThis interface will guarantee that the data is complete and valid before moving on to creating desired format.\nThe patch-data is internally stored as an numpy array to keep the data in an deep-learning framework agnostic format.\n\nThe library should provide all the necessary functionality via a CLI to allow for quick conversion without requiring to understand the details of the conversion process.\n\nAs of now, the only supported target format is the LMDB archive format.\n',
    'author': 'Kai Norman Clasen',
    'author_email': 'k.clasen@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai-tub/bigearthnet_encoder/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
