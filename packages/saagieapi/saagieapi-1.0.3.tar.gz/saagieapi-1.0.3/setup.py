# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['saagieapi',
 'saagieapi.apps',
 'saagieapi.docker_credentials',
 'saagieapi.env_vars',
 'saagieapi.jobs',
 'saagieapi.pipelines',
 'saagieapi.projects']

package_data = \
{'': ['*']}

install_requires = \
['croniter>=1.0.1,<2.0.0',
 'deprecation>=2.1.0,<3.0.0',
 'gql>=3.0.0,<4.0.0',
 'pytz>=2021.1,<2022.0',
 'requests>=2.27.0,<3.0.0',
 'requests_toolbelt>=0.9.1,<0.10.0']

setup_kwargs = {
    'name': 'saagieapi',
    'version': '1.0.3',
    'description': 'Python API to interact with Saagie',
    'long_description': '# Saagie api\n\n![Saagie api logo](https://github.com/saagie/api-saagie/blob/master/.github/banner.png?raw=true)\n\n[![PyPI version](https://img.shields.io/pypi/v/saagieapi?style=for-the-badge)](https://pypi.org/project/saagieapi/)\n![PyPI version](https://img.shields.io/pypi/pyversions/saagieapi?style=for-the-badge)\n\n[![GitHub release date](https://img.shields.io/github/release-date/saagie/api-saagie?style=for-the-badge&color=blue)][releases]\n\n[![Contributors](https://img.shields.io/github/contributors/saagie/api-saagie?style=for-the-badge&color=black)][contributors]\n![License](https://img.shields.io/pypi/l/saagieapi?style=for-the-badge&color=black)\n\n[releases]: https://github.com/saagie/api-saagie/releases\n\n[contributors]: https://github.com/saagie/api-saagie/graphs/contributors\n\n- [Presentation](#presentation)\n- [Installation](#installing)\n- [Usage](#usage)\n- [Contributing](#contributing)\n\n## Presentation\n\nThe `saagieapi` python package implements python API wrappers to easily interact with the Saagie platform in python.\n\n## Installing\n\n```bash\npip install saagieapi==<version>\n```\n\n### Compatibility with your Saagie platform\n\n| **Saagie platform version** | **saagie-api release** |\n|-----------------------------|------------------------|\n| < 2.2.0                     | < 0.6.0                |\n| >= 2.2.0                    | >= 0.6.0               |\n\n## Usage\n\nAll the implemented features are documented in the [Wiki](https://github.com/saagie/api-saagie/wiki)\n\nHere\'s a full example of how to use the API:\n\n```python\nfrom saagieapi import SaagieApi\n\nsaagie = SaagieApi(url_saagie="<url>",\n                   id_platform="1",\n                   user="<saagie-user-name>",\n                   password="<saagie-user-password>",\n                   realm="saagie")\n\n# Create a project named \'Project_test\' on the saagie platform\nproject_dict = saagie.projects.create(name="Project_test",\n                                     group="<saagie-group-with-proper-permissions>",\n                                     role=\'Manager\',\n                                     description=\'A test project\')\n\n# Save the project id\nproject_id = project_dict[\'createProject\'][\'id\']\n\n# Create a python job named \'Python test job\' inside this project\njob_dict = saagie.jobs.create(job_name="Python test job",\n                              project_id=project_id,\n                              file=\'<path-to-local-file>\',\n                              description=\'Amazing python job\',\n                              category=\'Processing\',\n                              technology_catalog=\'Saagie\',\n                              technology=\'python\',\n                              runtime_version=\'3.6\',\n                              command_line=\'python {file} arg1 arg2\',\n                              release_note=\'\',\n                              extra_technology=\'\')\n\n# Save the job id\njob_id = job_dict[\'data\'][\'createJob\'][\'id\']\n\n# Run the python job and wait for its completion\nsaagie.jobs.run_with_callback(job_id=job_id, freq=10, timeout=-1)\n\n```\n\n### Connecting to your platform\n\nThere are 2 options to connect to your platform :\n\n1. using the default constructor:\n\n    ```python\n    from saagieapi import *\n    saagie = SaagieApi(url_saagie="<url>",\n                       id_platform="1",\n                       user="<saagie-user-name>",\n                       password="<saagie-user-password>",\n                       realm="saagie")\n    ```\n\n2. Using the `easy_connect` alternative constructor which uses the complete URL (eg:\n    <https://mysaagie-workspace.prod.saagie.com/projects/platform/6/>) and will\n    parse it in order to retrieve the platform URL, platform id and the realm.\n\n    ```python\n    from saagieapi import *\n    saagie = SaagieApi.easy_connect(url_saagie_platform="<url>",\n                    user="<saagie-user-name>",\n                    password="<saagie-user-password>")\n    ```\n\nIf you want to know how to find the correct values for the URL, platform id and the realm,\nplease refer to the [Wiki](https://github.com/saagie/api-saagie/wiki#connecting-to-your-platform).\n\n## Contributing\n\nThe complete guide to contribute is available here:\n[Contributing](https://github.com/saagie/api-saagie/blob/master/CONTRIBUTING.md)\n',
    'author': 'Saagie',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/saagie/api-saagie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
