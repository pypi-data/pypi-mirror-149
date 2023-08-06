# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['caluma',
 'caluma.caluma_analytics',
 'caluma.caluma_analytics.management.commands',
 'caluma.caluma_analytics.migrations',
 'caluma.caluma_core',
 'caluma.caluma_core.management',
 'caluma.caluma_core.management.commands',
 'caluma.caluma_data_source',
 'caluma.caluma_form',
 'caluma.caluma_form.management',
 'caluma.caluma_form.management.commands',
 'caluma.caluma_form.migrations',
 'caluma.caluma_logging',
 'caluma.caluma_logging.management',
 'caluma.caluma_logging.management.commands',
 'caluma.caluma_logging.migrations',
 'caluma.caluma_user',
 'caluma.caluma_workflow',
 'caluma.caluma_workflow.migrations',
 'caluma.extensions',
 'caluma.settings']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.12,<4.0.0',
 'dateparser>=1.1.0,<2.0.0',
 'django-cors-headers>=3.11.0,<4.0.0',
 'django-environ>=0.8.1,<0.9.0',
 'django-extensions>=3.1.5,<4.0.0',
 'django-filter>=21.1,<22.0',
 'django-localized-fields>=6.6,<7.0',
 'django-postgres-extra>=2.0.4,<3.0.0',
 'django-simple-history>=3.0.0,<4.0.0',
 'django-watchman>=1.2.0,<2.0.0',
 'djangorestframework>=3.13.1,<4.0.0',
 'graphene-django>=3.0.0b7,<4.0.0',
 'graphql-core>=3.1.7,<3.2.0',
 'graphql-relay>=3.1.5,<4.0.0',
 'idna>=3.3,<4.0',
 'minio>=7.1.4,<8.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'pyjexl>=0.3.0,<0.4.0',
 'python-memcached>=1.59,<2.0',
 'requests>=2.27.1,<3.0.0',
 'uWSGI>=2.0.20,<3.0.0',
 'urllib3>=1.26.8,<2.0.0']

setup_kwargs = {
    'name': 'caluma',
    'version': '8.0.0b6',
    'description': 'Caluma Service providing GraphQL API',
    'long_description': "# ![Caluma Service](https://user-images.githubusercontent.com/6150577/60805422-51b1bf80-a180-11e9-9ae5-c794249c7a98.png)\n\n[![Build Status](https://github.com/projectcaluma/caluma/workflows/Tests/badge.svg)](https://github.com/projectcaluma/caluma/actions?query=workflow%3ATests)\n[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/projectcaluma/caluma/blob/main/setup.cfg#L57)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)\n[![PyPI](https://img.shields.io/pypi/v/caluma)](https://pypi.org/project/caluma/)\n[![License: GPL-3.0-or-later](https://img.shields.io/github/license/projectcaluma/caluma)](https://spdx.org/licenses/GPL-3.0-or-later.html)\n\nCaluma is a collaborative form editing and workflow service.\n\n- Website: [caluma.io](https://caluma.io)\n- Documentation: [caluma.gitbook.io](https://caluma.gitbook.io)\n\n## Getting started\n\n**Requirements**\n\n- docker\n- docker-compose\n\nAfter installing and configuring those, download [docker-compose.yml](https://github.com/projectcaluma/caluma/blob/main/docker-compose.yml) and run the following command:\n\n```bash\ndocker-compose up -d\n```\nSchema introspection and documentation is available at [http://localhost:8000/graphql](localhost:8000/graphql) and can be accessed using a GraphQL client such as [Altair](https://altair.sirmuel.design/). The API allows to query and mutate form and workflow entities which are described below.\n\nYou can read more about running and configuring Caluma in the [documentation](https://caluma.gitbook.io).\n\n## License\n\nCode released under the [GPL-3.0-or-later license](LICENSE).\n\nFor further information on our license choice, you can read up on the [corresponding GitHub issue](https://github.com/projectcaluma/caluma/issues/751#issuecomment-547974930).\n\n---\n\n- Contributing guide: [CONTRIBUTING.md](CONTRIBUTING.md)\n- Maintainer's Handbook: [MAINTAINING.md](MAINTAINING.md)\n",
    'author': 'Caluma',
    'author_email': 'info@caluma.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://caluma.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
