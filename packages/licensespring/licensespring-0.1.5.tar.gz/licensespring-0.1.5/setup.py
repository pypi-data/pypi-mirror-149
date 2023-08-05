# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['licensespring', 'licensespring.api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'licensespring',
    'version': '0.1.5',
    'description': 'LicenseSpring Python Library',
    'long_description': '# LicenseSpring Python Library\n\nThe LicenseSpring Python Library provides convenient access to the LicenseSpring API from\napplications written in the Python language.\n\n## Initialization\n\n### Poetry\n\nThis project uses [Poetry](https://python-poetry.org/) for packaging and dependency management.\nFor installation and usage see https://python-poetry.org/docs/.\n\nConfigure Poetry to create virtualenv inside the project’s root directory: \n```\npoetry config virtualenvs.in-project true\n```\n\nInstall dependencies: \n```\npoetry install\n```\n\n## Testing\n\nThis project uses [pytest](https://docs.pytest.org/en/7.1.x/) framework for testing.\n\nRun tests: \n```\npoetry run pytest\n```\n\n## Formatting\n\nThis project uses [black](https://github.com/psf/black) for code formatting.\n\nFormat code:\n```\npoetry run black .\n```\n\n## Building and Publishing\n\nThis project is published at [Python Package Index](https://pypi.org/).\n\nThe PyPI token must be configured in Poetry for publishing:\n```\npoetry config pypi-token.pypi {token}\n```\n\nMake sure to define new version before building and publishing.\n\nBuild the source and wheels archives:\n```\npoetry build\n```\n\nPublishes the package (previously built with the build command):\n```\npoetry publish\n```',
    'author': 'Toni Sredanović',
    'author_email': 'toni@licensespring.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://licensespring.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
