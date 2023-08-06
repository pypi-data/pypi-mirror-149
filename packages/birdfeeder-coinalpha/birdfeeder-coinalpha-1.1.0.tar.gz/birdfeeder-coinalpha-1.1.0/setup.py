# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['birdfeeder',
 'birdfeeder.aws',
 'birdfeeder.enum',
 'birdfeeder.pydantic',
 'birdfeeder.sqlalchemy']

package_data = \
{'': ['*'], 'birdfeeder': ['sample_configs/*']}

install_requires = \
['aioconsole>=0.1.16',
 'aiohttp>=3.2,<4.0',
 'aiorun>=2020,<2021',
 'boto3>=1,<2',
 'cachetools>=4,<5',
 'environs>=9,<10',
 'kafka-python>=2,<3',
 'pandas>=1.1,<2.0',
 'pydantic>=1.9.0,<2.0.0',
 'python-json-logger>=2,<3',
 'ruamel.yaml>=0.16,<0.17',
 'typer>=0.3']

entry_points = \
{'console_scripts': ['build_image = birdfeeder.build_image:app']}

setup_kwargs = {
    'name': 'birdfeeder-coinalpha',
    'version': '1.1.0',
    'description': 'Helper library for CoinAlpha projects',
    'long_description': '# birdfeeder\n\nHelper library for CoinAlpha projects\n\n## Usage\n\nThe library is published to pypi as [birdfeeder-coinalpha](https://pypi.org/project/birdfeeder-coinalpha/)\n\n### Installing\n\n```\npip install birdfeeder-coinalpha\n```\n\n```\npoetry add \'birdfeeder-coinalpha@^1\'\n```\n\n\n### How to install old versions\n\nIn pyproject.toml:\n\n```\nbirdfeeder-coinalpha = { git = "https://github.com/coinalpha/birdfeeder.git", branch = "master" }\nbirdfeeder-coinalpha = { git = "https://github.com/coinalpha/birdfeeder.git", rev = "29cdd7229d0d35a989322f5026382400d1332da4" }\nbirdfeeder-coinalpha = { git = "https://github.com/coinalpha/birdfeeder.git", tag = "0.1.0" }\n```\n\npip:\n\n```\ngit+https://github.com/coinalpha/birdfeeder.git@master#egg=birdfeeder\ngit+https://github.com/coinalpha/birdfeeder.git@29cdd7229d0d35a989322f5026382400d1332da4#egg=birdfeeder\ngit+https://github.com/coinalpha/birdfeeder.git@0.1.0#egg=birdfeeder\n```\n\n\n## Development\n\nTo install library for development in conda environment, run\n\n```\n./install\n```\n\nAlternativelly (preferred), you can use poetry env:\n\n```\npoetry install\npoetry shell\n```\n\n## How to add a dependency\n\n1. If you\'re running in conda, you need to install required package first.\n1. Then, see installed version in `conda env export`\n1. Take this version and add into pyproject.toml, into `[tool.poetry.dependencies]` (or dev section, if the package is needed for development only). Specify version (or range) according to [Dependency Specification](https://python-poetry.org/docs/dependency-specification/)\n\nIf using poetry:\n\n1. Run `poetry add <package>`\n\n## Releasing a new version\n\nIdea: we\'re keeping own version and dependencies info in `pyproject.toml`, and then generating `setup.py` so that the library could be installed via tools like pip. We\'re also generating `environment.yml` file because we\'re mostly using conda to manage development environments at CoinAlpha.\n\n1. Change version in `pyproject.toml` and `birdfeeder/__init__.py`\n1. Generate `setup.py`: `dephell deps convert`\n1. Generate `environment.yml`: `poetry2conda --dev pyproject.toml environment.yml`\n1. Commit updates `git add -u && git commit`\n1. Create git tag `x.y.z`: `git tag -s x.y.z`\n1. Run `git push && git push --tags`\n1. Publish to pypi: `poetry publish --build`\n',
    'author': 'Vladimir Kamarzin',
    'author_email': 'vvk@vvk.pp.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/coinalpha/birdfeeder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
