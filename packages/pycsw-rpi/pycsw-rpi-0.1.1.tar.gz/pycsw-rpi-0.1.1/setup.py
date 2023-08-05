# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycsw_rpi']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4,<2.0', 'pycsw>=2.6,<3.0']

entry_points = \
{'console_scripts': ['pycsw_rpi-admin = pycsw_rpi.admin:run']}

setup_kwargs = {
    'name': 'pycsw-rpi',
    'version': '0.1.1',
    'description': 'PyCSW monkey patched for Slovak national catalogue service',
    'long_description': '# PyCSW RPI `pycsw-rpi`\n\n[Monkey patched](https://en.wikipedia.org/wiki/Monkey_patch) `pycsw` for Slovak national catalogue service. \n\nCheck [original `pycsw` documentation ](https://docs.pycsw.org/en/2.6.1/index.html) for more details.\n\n---\n\n## Setup\n\nUse exactly like original `pycsw`\n\n### Install\n\n```bash\npip install --user pycsw-rpi\n```\n\n### Create configuration file\n\nConfiguration file is not distributed with package. \n\nSample configuration can be downloaded from `<<url>>`\n\n### Administrative command (CLI)\n\n`pycsw_rpi-admin` script is installed with package in `$PATH`, this script is replacement for original `pycsw-admin.py` script supporting modified beahaviour and can be used exactly like original one.\n\n#### Create database\n\n```bash\npycsw_rpi-admin -c setup_db -f <<pconfiguration_file>>\n```\n\n#### Load records\n\n```bash\npycsw_rpi-admin -c load_records -f <<pconfiguration_file>> -p <<path_to_records_directory>>\n```\n\nCheck [original documentation](https://docs.pycsw.org/en/2.6.1/administration.html) for `pycsw-admin.py` administrative command.\n\n### Run "dev" self contained (toy) server\n\n```bash\npython -m pycsw_rpi.wsgi\n```\n\n### Deploy as WSGI application\n\n`pycsw_rpi.wsgi` module contains WSGI `application` object (function) ready to be deployed with WSGI server (e.g. `gunicorn`, `uwsgi`). No WSGI server is installed with this package as dependecy. \n\nTo deploy with `gunicorn`:\n\n```bash\n# `gunicorn` package need to installed separately\npip install --user gunicorn\ngunicorn pycsw_rpi.wsgi:application\n```\n\n---\n\n## Modifications implemented (via monkey patches) to original `pycsw`\n\nAdded queryables to APISO plugin:\n- `rpi:OrganizationUUID`\n- `rpi:IsViewable`\n- `rpi:IsSearchable`\n\n---\n\n## Contributions\n\n',
    'author': 'Peter Mozolík',
    'author_email': 'petermozolik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mzpsr/minzp/geocloud.sk/applications/pycsw-rpi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
