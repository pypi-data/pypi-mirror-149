# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autoopen']

package_data = \
{'': ['*']}

extras_require = \
{'compressors': ['zstandard>=0.17.0,<0.18.0']}

setup_kwargs = {
    'name': 'autoopen',
    'version': '0.1.0',
    'description': 'Automatically compress or decompress files on open by filename.',
    'long_description': '# autoopen\n\n_autoopen_ is a small drop-in replacement for the most common use cases of Python’s built-in open() function that will automatically handle compressed files based on the filename.\n\n## Usage\n\nFor example:\n\n```python\nfrom autoopen import autoopen\n\nfilename = "example.txt.xz"\nwith autoopen(filename, "rt", encoding="utf-8") as file:\n    contents = file.read()\n```\n\n`autoopen` will check the given filename’s last suffix. If it indicates one of the supported compressors, the corresponding compressor or decompressor will be used, otherwise it falls back to built-in `open`. \n\nSupport for .gz, .bz2, .xz, .lzma, and .zst/.zstd is built-in (the latter requires the [python-zstandard](https://pypi.org/project/zstandard/) package). The special filename `-` indicates reading from stdin or writing to stdout.',
    'author': 'Thorsten Vitt',
    'author_email': 'tv@thorstenvitt.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thvitt/autoopen',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
