# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['civ4save']

package_data = \
{'': ['*']}

install_requires = \
['construct>=2.10.68,<3.0.0']

extras_require = \
{'xml': ['Jinja2>=3.1.2,<4.0.0', 'xmltodict>=0.12.0,<0.13.0']}

entry_points = \
{'console_scripts': ['civ4save = civ4save.cli:run']}

setup_kwargs = {
    'name': 'civ4save',
    'version': '0.1.0',
    'description': 'Extract data from a .CivBeyondSwordSave file',
    'long_description': "# Beyond the Sword Save File Reader\n\nUncompresses and decodes the data in a `.CivBeyondSwordSave` file.\ncheck out this [example](example.json) to see what data you can get.\n\nI've only tested with the vanilla version of the Civ4 BTS. Mods like BAT/BUG/BULL\nthat only change the interface should work but I need some example saves to test with.\nIf your mod changes the saved game format the parser will not work but if's there's\nenough demand to support a particular mod I'll make an effort to support it.\n\nThanks to [this repo](https://github.com/dguenms/beyond-the-sword-sdk) for hosting\nthe Civ4 BTS source. Wouldn't have been possible to make this without it.\n\n\n### Usage\n\n##### Developement Install\nUse this if you want to work on the code.\n\n1. clone the repo\n2. `poetry install`\n\n##### Lib/Cli Install\n\n`python -m pip install civ4save`\n\n##### Command line Tool\nOutput is JSON.\n\n`python -m civ4save <options> <save_file>`\n\n```\nusage: civ4save [-h] [--max-players MAX_PLAYERS]\n    [--with-plots | --just-settings | --just-players | --player PLAYER | --list-players]\n    file\n\nExtract data from .CivBeyondSwordSave file\n\npositional arguments:\n  file                  Target save file\n\noptions:\n  -h, --help            show this help message and exit\n  --max-players MAX_PLAYERS\n                        Needed if you have changed your MAX_PLAYERS value in CvDefines.h\n  --with-plots          Attempt to parse the plot data. WARNING: still buggy!\n  --just-settings       Only return the games settings. No game state or player data\n  --just-players        Only return the player data\n  --player PLAYER       Only return the player data for a specific player idx\n  --list-players        List all player idx, name, leader, civ in the game\n```\n\n##### As a Libray\n\n```python\nfrom civ4save import save_file\nfrom civ4save.structure import SaveFormat\n\nsave_bytes = save_file.read('path/to/save')\n\n# default max_players=19, you'll know if you changed this\ndata = SaveFormat.parse(save_bytes, max_players)\n\n# do whatever you want to with the data, see organize.py for ideas\n```\n\n### How it Works\nGames are saved in a binary format that kind of looks like a sandwich\n\n`| uncompressed data | zlib compressed data | uncompressed checksum |`\n\nwith most of the data in the compressed middle part. See `save_file.py` to understand\nhow the file is uncompressed.\n\nThen using the [construct](https://github.com/construct/construct) library the binary format\nis declaratively defined in `structure.py`.\n\nFrom there the functions in `organize.py` sort and cleanup the parsed data.\n\nThe enums defined in `cv_enums.py` are automatically generated from the game\nXML files using `xml_to_enum.py`. To run this yourself you'll need to install the optional\n`jinja2` and `xmltodict` dependencies:\n\n`poetry install -E xml`\n\nRight now the paths to the XML files in `xml_to_enum.py` are hardcoded so you'll have to edit\nthem to match your system.\n\n\n#### Write Order\nThe game calls it's `::write` functions in this order:\n\n1. CvInitCore\n2. CvGame\n3. CvMap\n4. CvPlot (incomplete/buggy)\n4. CvTeam (not implemented)\n5. CvPlayer (not implemented)\n\nBut there's issues consistently parsing `CvPlot` so only up to CvMap is parsed by default.\nI haven't drilled down the exact cause but it seems to have something to do with the size\nof the save file. Files under 136K (largest test save I have that works) parse fine but\nanything larger only makes it through ~30-80% of plots before failing.\n",
    'author': 'Dan Davis',
    'author_email': 'dan@dandavis.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
