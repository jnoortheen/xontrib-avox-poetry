# Overview

auto-activate venv as one cd into a poetry project folder. 

## Installation

To install use pip:

``` bash
xpip install xontrib-avox-poetry
# or: xpip install -U git+https://github.com/jnoortheen/xontrib-avox-poetry
```

## Usage

``` bash
xontrib load avox_poetry
```

## Configuration

```python

# If found, the env name is searched inside the $VIRTUALENV_HOME 
# rather than invoking `poetry env info -p` command every time `cd` happens
# It is faster setting this variable. It will also be used by poetry.
$VIRTUALENV_HOME = "~/.virtualenvs"

# name of the venv folder. If found will activate it.
# if set to None then local folder activation will not work.
$XSH_AVOX_VENV_NAME = ".venv"

# exclude activation of certain paths by setting
$XSH_AVOX_EXCLUDED_PATHS = {"xsh-src"}
```

## Credits

This package was created with [xontrib cookiecutter template](https://github.com/jnoortheen/xontrib-cookiecutter).
