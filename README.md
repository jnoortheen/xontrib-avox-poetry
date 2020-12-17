<p align="center">
auto-activate venv as one cd into a poetry project folder.
</p>

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
# name of the venv folder. If found will activate it.
# if set to None then local folder activation will not work.
$XSH_AVOX_VENV_NAME = ".venv"
```

## Credits

This package was created with [xontrib cookiecutter template](https://github.com/jnoortheen/xontrib-cookiecutter).
