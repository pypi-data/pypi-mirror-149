
# Config Development Environment

## Install Python

Tested on Ubuntu Ubuntu 20.04.4 LTS (64-bit) and Python 3.8.10.

```bash
# Confirm Python 3 is installed
$ python3 --version

Python 3.8.10

# Install venv
$ sudo apt install python3.8-venv

# Install pip
$ sudo apt install python3-pip
```

## Clone Repo

```bash
# Clone repo
$ git clone git@github.com:jay-law/job-scraper.git
$ cd job-scraper/

# Create new branch
$ git checkout -b BRANCH_NAME

# Create venv
$ python3 -m venv venv

# Activate venv
$ source venv/bin/activate

# Install requirements
$ python3 -m pip install -r requirements.txt

########################
# make changes to code
########################

# Update version in pyproject.toml

# Add modules as needed
$ python3 -m pip install SOME_NEW_MODULE

# Update requirements if modules were added
$ python3 -m pip freeze > requirements.txt

# Lint befor commiting
$ pylint *

# Add, commit, and push in git
$ git add *
$ git commit -m 'git commit message'
$ git push -u origin BRANCH_NAME

# Create a pull request
```

# Publishing

## Automatic

Merge your branch into the `test` branch.  GitHub actions will build and publish the package to [Test PyPI](https://test.pypi.org/project/exfill/).

If there are no errors, a second merge request can be created from `test` into `main` branch.  This workflow will publish to [PyPI](https://pypi.org/project/exfill/)

## Manual

It might be beneficial to manually publish a package.

```bash
# Install required tools
$ python3 -m pip install --upgrade build
$ python3 -m pip install --upgrade setuptools_scm
$ python3 -m pip install --upgrade twine

# Build 
$ python3 -m build

# Publish - test
$ python3 -m twine upload --repository testpypi --skip-existing dist/*

# Publish - prod
$ python3 -m twine upload --repository pypi --skip-existing dist/*
```

## Testing Published Package

```bash
$ mkdir python_test
$ cd python_test

# Create venv
$ python3 -m venv venv

# Activate venv
$ source venv/bin/activate

# Install from TestPyPI
# --extra-index-url helps with packages in prod but not test pypi
$ python3 -m pip install --extra-index-url https://test.pypi.org/simple/ exfill -U

# Or install from PyPI
$ python3 -m pip install --upgrade exfill

# Execute as mentioned in the README
```