"""

GetFX package
=============

Provides handling of FX rates using external FX API.

It submits request to external FX API, parse the response and prints it in
predefined manner. Each specific FX API provider requires new module based on
:py:mod:`getfx` (e.g. :py:mod:`getfx.getfxnbp` implements `NBP FX API
<http://api.nbp.pl/en.html>`_).

Modules:

- :py:mod:`getfx.getfx` - base functionality to be extended by specific API
- :py:mod:`getfx.getfxnbp` - specific NBP API implementation
- :py:mod:`getfx.cmdparser` - parsing command line interface

"""

__version__ = "0.1.8"
#: Defines minimum Python version, re-used in `setup.py`
__minPythonVersion__ = "3.7"
