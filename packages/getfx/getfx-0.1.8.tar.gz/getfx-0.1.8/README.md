# GetFX

GetFX is a tool to download average FX rates from National Bank of Poland
(NBP). All NBP exchange rates are to Polish Złoty (PLN).

| Check        	   | Result        |
| -------------    |:------------:|
| Build            | ![](https://github.com/kniklas/get-fx/workflows/build/badge.svg)|
| Coverage         | [![Coverage Status](https://coveralls.io/repos/github/kniklas/get-fx/badge.svg?branch=master&t=xgdvqo)](https://coveralls.io/github/kniklas/get-fx?branch=master)|

# Installation

If you have already installed Python, then simply use `pip install getfx` to install the package.

Prerequisites to install GetFX:
* [pip](https://pip.pypa.io/en/stable/installing/) 
* [setuptools](https://pypi.org/project/setuptools/)

Typically above applications are installed by default when you install python
from [python.org](https://www.python.org).

Alternatively you can install GetFX from this repository source code. After you
clone the repository execute from shell: `make build`.

More details on installation can be found in [documentation](https://kniklas.github.io/get-fx/installation.html)


# Usage

You can use the package from command line (example using Linux or MacOS):
* `getfx` - will return today FX from default currency (CHF)
* `getfx USD` - will return today FX for USD
* `getfx USD -d 2020-10-03` - will return USD FX on 3rd October 2020
* `getfx -h` - display help

Eventually you can run package using `python3` command:
* `python3 -m getfx` - same as first example above
* `python3 -m getfx USD` - same as second example above


# Documentation

If you would like to:
* deploy and develop this package please check [DEVELOPMENT.md](DEVELOPMENT.md)
* contribute to the project please check [CONTRIBUTING.md](CONTRIBUTING.md)
* read general purpose documentation please check: [documentation](https://kniklas.github.io/get-fx/)
