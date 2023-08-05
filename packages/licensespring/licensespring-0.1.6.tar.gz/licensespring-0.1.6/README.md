# LicenseSpring Python Library

The LicenseSpring Python Library provides convenient access to the LicenseSpring API from
applications written in the Python language.


## Initialization

### Poetry

This project uses [Poetry](https://python-poetry.org/) for packaging and dependency management.
For installation and usage see https://python-poetry.org/docs/.

Configure Poetry to create virtualenv inside the project’s root directory: 
```
poetry config virtualenvs.in-project true
```

Install dependencies: 
```
poetry install
```


## Testing

This project uses [pytest](https://docs.pytest.org/en/7.1.x/) framework for testing.

Run tests: 
```
poetry run pytest
```


## Formatting

This project uses [black](https://github.com/psf/black) for code formatting.

Format code:
```
poetry run black .
```


## Building and Publishing

This project is published at [Python Package Index](https://pypi.org/project/licensespring/).

The PyPI token must be configured in Poetry for publishing:
```
poetry config pypi-token.pypi {token}
```

Define the new version before building and publishing:
```
poetry version {version}
```

Build the source and wheels archives:
```
poetry build
```

Publishes the package (previously built with the build command):
```
poetry publish
```

A single command for both building and publishing is also possible:
```
poetry publish --build
```


## Installation

Install `licensespring` library:

```
pip install licensespring
```


## Usage

### Check license
```python
from licensespring.api import APIClient

api_client = APIClient(api_key="_your_api_key_", shared_key="_your_shared_key_")

license_data = api_client.check_license("_your_hardware_id_", "_your_license_key_", "_your_product_code_")

print(license_data)
```
