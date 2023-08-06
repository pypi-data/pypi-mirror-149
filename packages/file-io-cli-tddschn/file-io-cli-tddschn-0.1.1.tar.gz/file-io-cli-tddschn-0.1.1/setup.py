# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_io_cli_tddschn']

package_data = \
{'': ['*']}

install_requires = \
['clipboard>=0.0.4,<0.0.5', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['file.io-cli = file_io_cli_tddschn.file_io_cli:main']}

setup_kwargs = {
    'name': 'file-io-cli-tddschn',
    'version': '0.1.1',
    'description': 'Command-line tool to upload files to https://file.io',
    'long_description': "# file.io-cli\n\n    $ pip install file.io-cli\n\nCommand-line tool to upload files to https://file.io\n\n  [file.io]: https://www.file.io\n\n### Synopsis\n\n```\n$ file.io --help\nusage: file.io [-h] [--version] [-e E] [-n NAME] [-q] [-c] [-t PATH] [-z] [file]\n\nUpload a file to file.io and print the download link. Supports stdin.\n\npositional arguments:\n  file                  the file to upload\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --version             show program's version number and exit\n  -e E, --expires E     set the expiration time for the uploaded file\n  -n NAME, --name NAME  specify or override the filename\n  -q, --quiet           hide the progress bar\n  -c, --clip            copy the URL to your clipboard\n  -t PATH, --tar PATH   create a TAR archive from the specified file or directory\n  -z, --gzip            filter the TAR archive through gzip (only with -t, --tar)\n```\n\n### Examples\n\nUpload a file and copy the link:\n\n```\n$ file.io hello.txt -c\n[============================================================] 100% (15 bytes / 15 bytes)\nhttps://file.io/pgiPc2 (copied to clipboard)\n$ cat https://file.io/pgiPc2\nHello, File.io!\n```\n\nUpload a compressed archiveCompress a file/directory and upload it (streaming):\n\n```\n$ file.io -zt AllMyFiles/\n/ (55MB)\nhttps://file.io/sf2La\n```\n\nUpload from stdin:\n\n```\n$ find .. -iname \\*.py | file.io -n file-list.txt\n/ (312KB)\nhttps://file.io/uRglUT\n```\n\n### Changelog\n\n#### v1.0.4\n\n* Fix missing entrypoint in new setup script\n\n#### v1.0.3\n\n* Fix declared dependencies in setup script\n\n#### v1.0.2\n\n* Replaced `time.clock` (removed in python 3.8) with `time.perf_counter`\n* Minimum Python version is 3.3\n\n#### v1.0.1\n\n* Add `-t, --tar` and `-z, --gzip` options\n* Fix NameError when using `-c, --clip`\n* Fix progress bar left incomplete\n\n#### v1.0.0\n\n* Initial version\n",
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/file.io-cli-tddschn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
