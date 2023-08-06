# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daylio_parser']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22,<2.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'daylio-parser',
    'version': '0.4.1',
    'description': 'A Python module to parse Daylio exports',
    'long_description': '[![ci-badge][]][ci-link] [![docs-badge][]][docs-link]\n[![py-versions-badge][]][pypi-link] [![pypi-badge][]][pypi-link]\n\n# daylio-parser\n\nA Python module to parse Daylio CSV exports\n\n## Development\n\nInstall `poetry`, `tox` and `tox-poetry`.\n\nInstalling the virtual env:\n\n`$ poetry install`\n\nSwitching into the venv:\n\n`$ poetry shell`\n\nRunning test for the current python version:\n\n`$ pytest -v --cov=daylio_parser --cov-report term-missing tests`\n\nRunning all checks with tox prior to running GitHub actions:\n\n`$ tox`\n\n## TODO\n\n- [x] Parse CSV into entries (parser.py)\n- [x] Implement MoodConfig (config.py) to allow multiple moods\n    - [x] Plus a default config for clean Daylio installs\n- [ ] Stats\n    - [ ] Mood stability algorithm\n    - [x] Average moods by day\n    - [x] Average mood by activity\n    - [x] Find mood periods — aka periods of moods meeting certain criteria\n    - [ ] Extend mood period search — search above, below and in between thresholds\n- [x] Prepare data for plotting\n    - [x] Splitting entries into bands\n    - [x] Interpolating data for smooth charts\n    - [x] Calculating rolling mean\n- [ ] Re-export data into other formats\n    - [ ] JSON\n\n[ci-link]: https://github.com/staticf0x/daylio-parser/actions/workflows/check.yml\n[ci-badge]: https://img.shields.io/github/workflow/status/staticf0x/daylio-parser/Check/master\n[docs-link]: https://daylio-parser.readthedocs.io/en/latest/\n[docs-badge]: https://img.shields.io/readthedocs/daylio-parser/latest\n[py-versions-badge]: https://img.shields.io/pypi/pyversions/daylio-parser\n[pypi-link]: https://pypi.org/project/daylio-parser/\n[pypi-badge]: https://img.shields.io/pypi/v/daylio-parser\n',
    'author': 'staticf0x',
    'author_email': '44530786+staticf0x@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/staticf0x/daylio-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
