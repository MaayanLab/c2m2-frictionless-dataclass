# frictionless-dataclass

This script enables construction of python dataclass from datapackages, this is useful to provide autocompletion from python.

## Installation
```bash
pip3 install "frictionless-dataclass @ git+https://github.com/nih-cfde/c2m2-frictionless-dataclass#egg=frictionless-dataclass&subdirectory=frictionless-dataclass"
```

## Usage
```bash
# Generate python code [schema.py] for the given datapackage.json
frictionless-dataclass -i datapackage.json -o schema.py
```
