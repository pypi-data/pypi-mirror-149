# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['viz_manga']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0', 'viz-image-unobfuscate>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'viz-manga',
    'version': '0.1.1',
    'description': 'Viz Manga Reader',
    'long_description': '# Viz Manga Viewer\nRetrieves and unobfuscates manga pages for an input chapter id. Manga pages can be saves the dual spread images as well as single page images. Chapter ids need to be retrieved from the Viz site by looking at the chapter url.\n\nDISCLAIMER: I am not licensed or affiliated with Viz Media and this repository is meant for informational purposes only. Please delete the retrieved pages after reading.\n\n# Installation\n```\npip install viz_manga\n```\n\n# Usage\n```\nusage: manga.py [-h] [--directory DIRECTORY] [--combine] chapter_id\n\nUnobfuscates an entire manga chapter for reading.\n\npositional arguments:\n  chapter_id            Chapter id obtained from the Viz site.\n\noptions:\n  -h, --help            show this help message and exit\n  --directory DIRECTORY\n                        Output directory to save the unobfuscated pages.\n  --combine             Combine left and right pages into one image.\n```\n\n# Example\n```\n>>> python manga.py 24297 --directory images/ --combine\n\nINFO:root:Getting 20 pages for One Piece Chapter 1047.0\nSuccessfully retrieved chapter 24297\n\n```\n\n# Docker\n```\n>>> docker build -t viz-manga .\n>>> docker run -v /home/user/images/:/app/images viz-manga  24297 --directory images/ --combine\n\nINFO:root:Getting 20 pages for One Piece Chapter 1047.0\nSuccessfully retrieved chapter 24297\n\n```',
    'author': 'Kevin Ramdath',
    'author_email': 'krpent@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/minormending/viz-manga',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
