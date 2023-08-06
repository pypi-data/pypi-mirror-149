# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyheadspace']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.3.0,<3.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'requests>=2.26.0,<3.0.0',
 'rich>=12.2.0,<13.0.0']

entry_points = \
{'console_scripts': ['headspace = pyheadspace.__main__:cli']}

setup_kwargs = {
    'name': 'pyheadspace',
    'version': '3.1.5',
    'description': 'Command line script to download packs and singles from Headspace.',
    'long_description': '# headspace-cli\n[![PyPI version](https://badge.fury.io/py/pyheadspace.svg)](https://badge.fury.io/py/pyheadspace)\n\nCommand line script to download headspace packs, singles or everyday meditation.\n<p align="center">\n\n<img src = "https://user-images.githubusercontent.com/57002207/147270294-de0ec3f9-7bfa-4c63-84de-b4239fd4995e.gif" alt = "demo">\n</p>\n\n\n\n- [👶 Dependencies](#-dependencies)\n- [🛠️ Installation](#️-installation)\n- [⚙️ Setup](#️-setup)\n- [🚀 Usage](#-usage)\n\n\n\n## 👶 Dependencies\n* [Python 3.7 or higher](https://www.python.org/downloads/)\n\n## 🛠️ Installation\n```sh\npip install --upgrade pyheadspace\n```\n* If installing using `pip install --user`, you must add the user-level bin directory to your PATH environment variable in order to use pyheadspace. If you are using a Unix derivative (FreeBSD, GNU / Linux, OS X), you can achieve this by using `export PATH="$HOME/.local/bin:$PATH"` command.\n\n\n**OR install with [pipx](https://github.com/pypa/pipx)**\n\n\n```sh\npipx install pyheadspace\n```\n\n### This tool is only meant for personal use. Do not use this for piracy!\n## ⚙️ Setup\n\nRun and enter login credentials.\n```sh\nheadspace login\n```\nIf you use other form of authentication like google(do not have username and password), you could follow\n[these steps](https://github.com/yashrathi-git/pyHeadspace/blob/main/manual_setup.md)\n\n \n\n## 🚀 Usage\n\n## Download all packs at once\n```sh\n# Download all packs with each session of duration 15 minutes\nheadspace pack --all --duration 15\n\n# Download all packs with session duration of 10 & 20 minutes\nheadspace pack --all --duration 10 --duration 15\n```\n**Exclude specific packs from downloading:**\n<br />\n\nTo exclude specific packs from downloading use `--exclude` option.\n<br />\nIt expects location of text file for links of packs to exclude downloading. Every link should be on separate line.<br><br>\n**links.txt**:\n```\nhttps://my.headspace.com/modes/meditate/content/154\nhttps://my.headspace.com/modes/meditate/content/150\n```\n**command**\n```sh\nheadspace packs --all --exclude links.txt\n```\nThis would download all packs except the ones in `links.txt` file\n\n## Downloading specific pack\n```sh\nheadspace pack <PACK_URL> [Options]\n```\n\n<br />\n\n**BASIC USAGE**\n```sh\n# Download with all session of duration 15 minutes\nheadspace pack https://my.headspace.com/modes/meditate/content/151 --duration 15 \n\n# Download sessions of multiple duration\nheadspace pack https://my.headspace.com/modes/meditate/content/151 -d 20 -d 15   \n\n```\n**Options:**\n```sh\n--id INTEGER         ID of video.\n-d, --duration TEXT  Duration or list of duration\n--no_meditation      Only download meditation session without techniques\n                    videos.\n--no_techniques      Only download techniques and not meditation sessions.\n--out TEXT           Download directory\n--all                Downloads all headspace packs.\n-e, --exclude TEXT   Use with `--all` flag. Location of text file with links\n                    of packs to exclude downloading. Every link should be\n                    on separate line.\n--help               Show this message and exit.\n\n```\n\n## Download single session\n```sh\nheadspace download <SESSION_URL> [options]\n```\n\n\n<br />\n\n**BASIC USAGE**\n```sh\n$ headspace download https://my.headspace.com/player/204?authorId=1&contentId=151&contentType=COURSE&mode=meditate&trackingName=Course&startIndex=1 --duration 15\n```\n**Options:**\n```sh\n--out TEXT           Download directory.\n--id INTEGER         ID of the video. Not required if URL is provided.\n-d, --duration       Duration or list of duration\n--help               Show this message and exit.\n```\n\n\n## Download everyday meditations\n```sh\nheadspace everyday [OPTIONS]\n```\n\n\n**BASIC USAGE**\n```sh\n# Downloads today\'s meditation\nheadspace everyday\n\n# Download everyday meditation of specific time period.\n# DATE FORMAT: yyyy-mm-dd\nheadspace everyday --from 2021-03-01 --to 2021-03-20\n```\n**Options**\n```\n--from TEXT          Start download from specific date. DATE-FORMAT=>yyyy-\n                    mm-dd\n--to TEXT            Download till a specific date. DATE-FORMAT=>yyyy-mm-dd\n-d, --duration TEXT  Duration or list of duration\n--out TEXT           Download directory\n--help               Show this message and exit.\n```\n\n## Changing Language Preference\nBy default the language is set to english. You could change to other languages supported by headspace. \nOther Languages:\n- de-DE\n- es-ES\n- fr-FR\n- pt-BR\n\nTo change the language modify the environment variable `HEADSPACE_LANG` and set the value to the langauge code.\n\n- For fish/bash shell `export HEADSPACE_LANG="fr-FR"`\n- Powershell `$env:DESIRED_LANGUAGE="fr-FR"`\n\n\n\n\n\n\n\n**If you encounter any issue or bug, open a new issue on [github](https://github.com/yashrathi-git/pyHeadspace)**\n\n\n\n',
    'author': 'Yash Rathi',
    'author_email': 'yashrathicricket@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yashrathi-git/pyHeadspace',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
