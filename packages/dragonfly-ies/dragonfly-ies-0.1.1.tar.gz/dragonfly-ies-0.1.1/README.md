[![Build Status](https://github.com/ladybug-tools/dragonfly-ies/workflows/CI/badge.svg)](https://github.com/ladybug-tools/dragonfly-ies/actions)

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

# dragonfly-ies

Dragonfly extension for export to IES-VE GEM file format

## Installation
```console
pip install dragonfly-ies
```

## QuickStart
```python
import dragonfly_ies

```

## [API Documentation](http://ladybug-tools.github.io/dragonfly-ies/docs)

## Local Development
1. Clone this repo locally
```console
git clone git@github.com:ladybug-tools/dragonfly-ies

# or

git clone https://github.com/ladybug-tools/dragonfly-ies
```
2. Install dependencies:
```console
cd dragonfly-ies
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

3. Run Tests:
```console
python -m pytest tests/
```

4. Generate Documentation:
```console
sphinx-apidoc -f -e -d 4 -o ./docs ./dragonfly_ies
sphinx-build -b html ./docs ./docs/_build/docs
```
