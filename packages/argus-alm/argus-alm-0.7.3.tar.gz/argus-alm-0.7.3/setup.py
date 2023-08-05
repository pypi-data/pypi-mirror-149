# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argus',
 'argus.backend',
 'argus.backend.controller',
 'argus.backend.service',
 'argus.db']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'scylla-driver>=3.24.8,<4.0.0']

setup_kwargs = {
    'name': 'argus-alm',
    'version': '0.7.3',
    'description': 'Argus',
    'long_description': '# Argus\n\n## Description\n\nArgus is a test tracking system intended to provide observability into automated test pipelines which use long-running resources. It allows observation of a test status, its events and its allocated resources. It also allows easy comparison between particular runs of a specific test.\n\n## Installation notes\n\n### Prerequisites\n\n- Python >=3.10.0 (system-wide or pyenv)\n\n- NodeJS >=16 (with npm)\n\n- Yarn (can be installed globally with `npm -g install yarn`)\n\n- nginx\n\n- pyenv\n\n- pyenv-virtualenv\n\n### From source\n\n#### Production\n\nPerform the following steps:\n\nCreate a user that will be used by uwsgi:\n\n```bash\nuseradd -m -s /bin/bash argus\nsudo -iu argus\n```\n\nInstall pyenv and create a virtualenv for this user:\n\n```bash\npyenv install 3.10.0\npyenv virtualenv argus\npyenv activate argus\n```\n\nClone the project into a directory somewhere where user has full write permissions\n\n```bash\ngit clone https://github.com/bentsi/argus ~/app\ncd ~/app\n```\n\nInstall project dependencies:\n\n```bash\npip install -r requirements_web.txt\npip install -e .\nyarn install\n```\n\nCompile frontend files from `/frontend` into `/public/dist`\n\n```bash\nyarn webpack\n```\n\nCreate a `argus.local.yaml` configuration file (used to configure database connection) and a `argus_web.yaml` (used for webapp secrets) in your application install directory.\n\n```bash\ncp argus_web.example.yaml argus_web.yaml\ncp argus.yaml argus.local.yaml\n```\n\nOpen `argus.local.yaml` and add the database connection information (contact_points, user, password and keyspace name).\n\nOpen `argus_web.yaml` and change the `SECRET_KEY` value to something secure, like a sha512 digest of random bytes. Fill out GITHUB_* variables with their respective values.\n\nCopy nginx configuration file from `docs/configs/argus.nginx.conf` to nginx virtual hosts directory:\n\nUbuntu:\n\n```bash\nsudo cp docs/configs/argus.nginx.conf /etc/nginx/sites-available/argus\nsudo ln -s /etc/nginx/sites-enabled/argus /etc/nginx/sites-available/argus\n```\n\nRHEL/Centos/Alma/Fedora:\n\n```bash\nsudo cp docs/configs/argus.nginx.conf /etc/nginx/conf.d/argus.conf\n```\n\nAdjust the webhost settings in that file as necessary, particularly `listen` and `server_name` directives.\n\nCopy systemd service file from `docs/config/argus.service` to `/etc/systemd/system` directory:\n\n```bash\nsudo cp docs/config/argus.service /etc/systemd/system\n```\n\nOpen it and adjust the path to the `start_argus.sh` script in the `ExecStart=` directive and the user/group, then reload systemd daemon configuration and enable (and optionally start) the service.\n\nWARNING: `start_argus.sh` assumes pyenv is installed into `~/.pyenv`\n\n```bash\nsudo systemctl daemon-reload\nsudo systemctl enable --now argus.service\n```\n\n#### Development\n\nInstall pyenv and create a virtualenv for argus:\n\n```bash\npyenv install 3.10.0\npyenv virtualenv argus\npyenv activate argus\n```\n\nClone the project into a directory somewhere\n\n```bash\ngit clone https://github.com/bentsi/argus\ncd argus\n```\n\nInstall project dependencies:\n\n```bash\npip install -r requirements_web.txt\npip install -e .\nyarn install\n```\n\nCompile frontend files from `/frontend` into `/public/dist`. Add --watch to recompile files on change.\n\n```bash\nyarn webpack --watch\n```\n\nCreate a `argus.local.yaml` configuration file (used to configure database connection) and a `argus_web.yaml` (used for webapp secrets) in your application install directory.\n\n```bash\ncp argus_web.example.yaml argus_web.yaml\ncp argus.yaml argus.local.yaml\n```\n\nOpen `argus.local.yaml` and add the database connection information (contact_points, user, password and keyspace name).\n\nOpen `argus_web.yaml` and change the `SECRET_KEY` value to something secure, like a sha512 digest of random bytes. Fill out GITHUB_* variables with their respective values.\n\nRun the application from CLI using:\n\n```bash\nFLASK_ENV="development" FLASK_APP="argus.backend" FLASK_DEBUG=1 flask run\n```\n\nOmit `FLASK_DEBUG` if running your own debugger (pdb, pycharm, vscode)\n',
    'author': 'Alexey Kartashov',
    'author_email': 'alexey.kartashov@scylladb.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/scylladb/argus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
