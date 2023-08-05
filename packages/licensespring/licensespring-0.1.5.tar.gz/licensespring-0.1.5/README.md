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

This project is published at [Python Package Index](https://pypi.org/).

The PyPI token must be configured in Poetry for publishing:
```
poetry config pypi-token.pypi {token}
```

Make sure to define new version before building and publishing.

Build the source and wheels archives:
```
poetry build
```

Publishes the package (previously built with the build command):
```
poetry publish
```