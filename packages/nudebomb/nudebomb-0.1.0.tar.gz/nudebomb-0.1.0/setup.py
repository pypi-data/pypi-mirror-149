# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nudebomb', 'tests']

package_data = \
{'': ['*'], 'tests': ['mockdata/*', 'test_files/*']}

install_requires = \
['confuse>=1.7.0,<2.0.0',
 'pycountry>=22.3.5,<23.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'termcolor>=1.1.0,<2.0.0',
 'treestamps>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['nudebomb = nudebomb.cli:main']}

setup_kwargs = {
    'name': 'nudebomb',
    'version': '0.1.0',
    'description': 'Strip unused languages from mkv files en mass',
    'long_description': "# Nudebomb\n\nThe Nudebomb recursively strips matroska media files of unwanted audio and\nsubtitle tracks.\n\n## News\n\nYou may find user focused nudebomb changes in the [NEWS file](https://github.com/ajslater/nudebomb/tree/NEWS.md).\n\n## Requirements\n\n- MKVToolNix\n- Python3\n\n## Install\n\n    pip install\n\n## Usage\n\n### Posix\n\n    nudebomb -rl eng,fre /mnt/movies\n\n### Windows\n\n    nudebomb -b C:\\\\Program/ Files\\MKVToolNix\\mkvmerge.exe -rl eng,jap \\\\nas\\movies\n\n## Config\n\nYou may configure Nudebomb options via the command, a yaml config file\nand environment variables.\n\n### Environment variable format\n\nPrefix environment variables with `NUDEBOMB_NUDEBOMB__` and enumerate lists elements:\n\n```sh\nNUDEBOMB_NUDEBOMB__RECURSE=True\nNUDEBOMB_NUDEBOMB__LANGUAGES__0=und\nNUDEBOMB_NUDEBOMB__LANGUAGES__1=eng\n```\n\n## Lang Files\n\nWhile you may have a primary language, you probably want videos from other countries to keep\ntheir native language as well. Lang files let you do this.\n\nLang files are persistent files on disk that nudebomb parses to keep to all languages in\nthem in the mkvs in the current directory and all mkvs in sub directories.\n\nValid lang file names are: 'lang', 'langs', '.lang', or '.langs'\nThey include comma separated list of languages to keep like the `-l` option.\n\ne.g. You may have an entire collecttion of different TV shows with a root lang file\ncontaining the `eng` language. Under that directory you may have a specifi TV show directory\nwith lang file containing `jpn`. All mkvs in season directories under that would then\nkeep both the `eng` and `jpn` languages, while other TV shows would keep only `eng` languages.\n\nFor each mkv file, nudebomb looks up the directory tree for each parent lang file and uses the\nunion of all languages found to determine what languages to keep.\n\n### APIs\n\nLangfiles would be obsolete if nudebomb could deterimining native languages for mkv files by\npolling and caching results from major online media databases. It's the right thing to do, but I\ndon't care to implement it. Patches or forks welcome.\n\n## Inspiration\n\nNudebomb is a radical fork of [mkvstrip](https://github.com/willforde/mkvstrip). It adds recursion, lang files, timestamps and more configuration to mkvstrip and fixes some minor bugs.\n",
    'author': 'AJ Slater',
    'author_email': 'aj@slater.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ajslater/nudebomb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
