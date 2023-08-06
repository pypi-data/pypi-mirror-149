# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vt2m', 'vt2m.lib', 'vt2m.subcommands']

package_data = \
{'': ['*']}

install_requires = \
['pymisp>=2.4.155',
 'requests>=2.27.1,<3.0.0',
 'typer>=0.4.1,<0.5.0',
 'vt-py>=0.14.0,<0.15.0']

entry_points = \
{'console_scripts': ['vt2m = vt2m.main:app']}

setup_kwargs = {
    'name': 'vt2m',
    'version': '0.1.5',
    'description': 'Automatically import results from VirusTotal queries into MISP objects',
    'long_description': '# VirusTotal Query to MISP Objects (vt2m)\n\nWhile there are multiple Python projects which implement the object creation based on single VirusTotal objects, this\nproject aims to enable users to directly convert VirusTotal search queries to MISP objects.\n**This is work in progress.** Future release will implement handling URLs, Domain and IP objects, too. Right now, only\nfile objects are implemented.\n\n## Installation\n\n```\npip install vt2m\n```\n\n## Usage\n\nIf you use the script frequently, passing the arguments as environment variables (`MISP_URL`, `MISP_KEY`, `VT_KEY`)\ncan be useful to save some time. For example, this can be achieved through creating a shell script which passes the\nenvironment variables and executes the command with spaces in front, so it does not show up in the shell history.\n\nVia `--relations` VirusTotal relations can be resolved and added as MISP objects with the specific relations, e.g. the\nfollowing graph was created using vt2m:\n![MISP Graph](.github/screenshots/graph.png)\n*Graph created via `vt2m --uuid <UUID> --limit 5 --relations dropped_files,execution_parents "behaviour_processes:\\"ping -n 70\\""`*\n\n### Params\n```\nusage: vt2m [-h] --uuid UUID [--url URL] [--key KEY] [--vt-key VT_KEY] [--comment COMMENT] [--limit LIMIT] [--relations RELATIONS] [--quiet]\n            [--detections DETECTIONS]\n            query\n\npositional arguments:\n  query                 VT query\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --uuid UUID, -u UUID  MISP event uuid\n  --url URL, -U URL     MISP URL - can also be given as env MISP_URL\n  --key KEY, -k KEY     MISP API key - can also be given as env MISP_KEY\n  --vt-key VT_KEY, -K VT_KEY\n                        VT API key - can also be given as env VT_KEY\n  --comment COMMENT, -c COMMENT\n                        Comment to add to MISP objects\n  --limit LIMIT, -l LIMIT\n                        Limit results of VT query - default is 100\n  --relations RELATIONS, -r RELATIONS\n                        Comma-seperated list of relations to request PER result (if type fits). This can burn your API credits. Currently\n                        implemented: dropped_files, executing_parents, bundled_files\n  --quiet, -q           Disable output. Stderr will still be printed.\n  --detections DETECTIONS, -d DETECTIONS\n                        Only consider related entities with at least X malicious detections.\n```\n',
    'author': '3c7',
    'author_email': '3c7@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/3c7/vt2m',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
