# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openmldb_exporter', 'openmldb_exporter.collector']

package_data = \
{'': ['*']}

install_requires = \
['Twisted>=22.2.0,<23.0.0',
 'openmldb>=0.5.0,<0.6.0',
 'prometheus-client>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['openmldb-exporter = openmldb_exporter.exporter:main']}

setup_kwargs = {
    'name': 'openmldb-exporter',
    'version': '0.5.0a0',
    'description': 'prometheus exporter for OpenMLDB',
    'long_description': '# OpenMLDB Prometheus Exporter\n\n## Intro\n\nThis directory contains\n\n1. OpenMLDB Exporter exposing prometheus metrics\n2. OpenMLDB mixin provides well-configured examples for prometheus server and grafana dashboard\n\nSupported versions:\n\n+ OpenMLDB >= 0.5.0\n\n## Development\n\n### Requirements\n\n- Python >= 3.8 \n- [poetry](https://github.com/python-poetry/poetry) as build tool\n- cmake (optional if want to test latest commit)\n- a runnable OpenMLDB instance that is accessible from your network\n\n### Build\n\nThe exporter is a python project, the only thing need to built was the native library required by python sdk. To build, `cd` to root directory of OpenMLDB, and run:\n\n```bash\nmake SQL_PYSDK_ENABLE=ON\n```\n\nNote: build is only required when tesing over latest commit is needed, otherwise, it can installed directly from pip (when 0.5.0 released):\n\n```bash\npip install openmldb-exporter==0.5.0\n```\n\n### Run\n\n1. setup python dependencies:\n\n   ```bash\n   poetry install\n   ```\n\n2. enter virtual environment\n\n   ```bash\n   poetry shell\n   ```\n\n3. start openmldb exporter\n\n   ```bash\n   poetry run openmldb-exporter\n   ```\n\n   you need pass necessary flags after `openmldb-exporter`. run `poetry run openmldb-exporter --help` to get the help info\n\n   ```bash\n   usage: openmldb-exporter [-h] [--log.level LOG.LEVEL] [--web.listen-address WEB.LISTEN_ADDRESS]\n                            [--web.telemetry-path WEB.TELEMETRY_PATH] [--config.zk_root CONFIG.ZK_ROOT]\n                            [--config.zk_path CONFIG.ZK_PATH] [--config.interval CONFIG.INTERVAL]\n   \n   OpenMLDB exporter\n   \n   optional arguments:\n     -h, --help            show this help message and exit\n     --log.level LOG.LEVEL\n                           config log level, default WARN\n     --web.listen-address WEB.LISTEN_ADDRESS\n                           process listen port, default 8000\n     --web.telemetry-path WEB.TELEMETRY_PATH\n                           Path under which to expose metrics, default metrics\n     --config.zk_root CONFIG.ZK_ROOT\n                           endpoint to zookeeper, default 127.0.0.1:6181\n     --config.zk_path CONFIG.ZK_PATH\n                           root path in zookeeper for OpenMLDB, default /\n     --config.interval CONFIG.INTERVAL\n                           interval in seconds to pull metrics periodically, default 30.0\n   ```\n\n4. view the available metrics, you can pull through `curl`\n\n   ```bash\n   curl http://127.0.0.1:8000/metrics\n   ```\n\n   a example output:\n\n   ```bash\n   # HELP openmldb_connected_seconds_total duration for a component conncted time in seconds                              \n   # TYPE openmldb_connected_seconds_total counter                                                                        \n   openmldb_connected_seconds_total{endpoint="172.17.0.15:9520",role="tablet"} 208834.70900011063                         \n   openmldb_connected_seconds_total{endpoint="172.17.0.15:9521",role="tablet"} 208834.70700001717                         \n   openmldb_connected_seconds_total{endpoint="172.17.0.15:9522",role="tablet"} 208834.71399998665                         \n   openmldb_connected_seconds_total{endpoint="172.17.0.15:9622",role="nameserver"} 208833.70000004768                     \n   openmldb_connected_seconds_total{endpoint="172.17.0.15:9623",role="nameserver"} 208831.70900011063                     \n   openmldb_connected_seconds_total{endpoint="172.17.0.15:9624",role="nameserver"} 208829.7230000496                      \n   # HELP openmldb_connected_seconds_created duration for a component conncted time in seconds                            \n   # TYPE openmldb_connected_seconds_created gauge                                                                        \n   openmldb_connected_seconds_created{endpoint="172.17.0.15:9520",role="tablet"} 1.6501813860467942e+09                   \n   openmldb_connected_seconds_created{endpoint="172.17.0.15:9521",role="tablet"} 1.6501813860495396e+09                   \n   openmldb_connected_seconds_created{endpoint="172.17.0.15:9522",role="tablet"} 1.650181386050323e+09                    \n   openmldb_connected_seconds_created{endpoint="172.17.0.15:9622",role="nameserver"} 1.6501813860512116e+09               \n   openmldb_connected_seconds_created{endpoint="172.17.0.15:9623",role="nameserver"} 1.650181386051238e+09                \n   openmldb_connected_seconds_created{endpoint="172.17.0.15:9624",role="nameserver"} 1.6501813860512598e+09               \n   ```\n',
    'author': 'aceforeverd',
    'author_email': 'teapot@aceforeverd.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://openmldb.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
