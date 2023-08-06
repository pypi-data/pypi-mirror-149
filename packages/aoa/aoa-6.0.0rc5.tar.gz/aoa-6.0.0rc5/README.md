# AnalyticOps Accelerator Python Client
[![Build Status](https://dev.azure.com/teradata-consulting/AnalyticOps/_apis/build/status/ThinkBigAnalytics.AoaPythonClient?branchName=master)](https://dev.azure.com/teradata-consulting/AnalyticOps/_build/latest?definitionId=94&branchName=master)
![PyPI](https://img.shields.io/pypi/v/aoa)

Python client for Teradata AnalyticOps Accelerator. It is composed of both an client API implementation to access the AOA Core APIs and a command line interface (cli) tool which can be used for many common tasks. 


## Requirements

Python 3.5+


## Usage

See the pypi [guide](./docs/pypi.md) for some usage notes. 


## Installation

To install the latest release, just do

```bash
pip install aoa
```

To build from source, it is advisable to create a Python venv or a Conda environment 

Python venv:
```bash
python -m venv aoa_python_env
source aoa_python_env/bin/activate
```

Conda environment:
```bash
conda create -n aoa_python_env -q -y python=3.6
conda activate aoa_python_env
```

Install library from local folder using pip:

```bash
pip install --upgrade .
```

Install library from package file

```bash
# first create the package
python setup.py clean --all
python setup.py sdist bdist_wheel

# install using pip
pip install dist/*.whl
```

Bash autocomplete for `aoa` utility:
```bash
eval "$(register-python-argcomplete aoa)"
```
## Testing

```bash
pip install -r dev_requirements.txt
python -m pytest
```

## Building and releasing 

```bash
python -m pip install --user --upgrade setuptools wheel twine

rm -rf dist/ 

python setup.py sdist bdist_wheel

twine upload -u td-aoa -p <user@pass> dist/*

```
