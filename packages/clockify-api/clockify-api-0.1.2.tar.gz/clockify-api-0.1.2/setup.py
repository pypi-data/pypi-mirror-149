# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clockify', 'clockify.apis', 'clockify.model']

package_data = \
{'': ['*']}

install_requires = \
['bidict>=0.22.0,<0.23.0',
 'marshmallow>=3.15.0,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'clockify-api',
    'version': '0.1.2',
    'description': "Python wrapper for Clockify's API.",
    'long_description': '![GitHub Workflow Status](https://img.shields.io/github/workflow/status/jpweijers/clockify-api/CI)\n[![Coverage Status](https://coveralls.io/repos/github/jpweijers/clockify-api/badge.svg?branch=main)](https://coveralls.io/github/jpweijers/clockify-api?branch=main)\n[![Documentation Status](https://readthedocs.org/projects/clockify-api/badge/?version=latest)](https://clockify-api.readthedocs.io/en/latest/?badge=latest)\n\n# Clockify\n\n## Documentation\n\n- [Package Documentation](clockify-api.readthedocs.io)\n- [Official Clocify API reference](https://clockify.me/developers-api)\n\n## Installation\n\n```bash\n# Pip\npip install clockify-api\n\n# Poetry\npoetry add clockify-api\n```\n\n## Example Usage\n\n```python\nfrom clockify.session import ClockifySession\n\nKEY = "YOUR_API KEY"\nWORKSPACE = "YOUR WORKSPACE ID"\n\nclockify_session = ClockifySession(KEY)\n\nprojects = clockify_session.project.get_projects(WORKSPACE)\n\nfor project in projects:\n    print(f"Project {project.name}, Client: {project.client_name}")\n```\n',
    'author': 'Jean-Paul Weijers',
    'author_email': 'jpweijers@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jpweijers/clockify-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
