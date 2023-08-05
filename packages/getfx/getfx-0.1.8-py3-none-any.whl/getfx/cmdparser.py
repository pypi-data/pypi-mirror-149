"""

Command line parser module
==========================

Module implements specific command line parsing in :py:func:`parse_getfx()`
function and defines / uses constant: :py:const:`DEFAULT_CURRENCY`.

"""

import argparse as ap
import getfx

#: Default currency if not given
DEFAULT_CURRENCY = "CHF"


def parse_getfx(test_args=None):
    """Initialize argparse parser object and return parsed arguments.

    :keyword test_args: used as alternative to patch ``parse_args``
        or ``sys.argv`` for unit testing. Argument value ``None`` is used in
        real implementation (not unit testing).
    :returns: ``Namespace`` object with parsed arguments, for example

    >>> args=['USD', '-d', '2020-10-10']
    >>> parse_getfx(args)
    Namespace(currency='USD', date='2020-10-10')
    >>> parse_getfx(args).currency
    'USD'
    >>> parse_getfx(args).date
    '2020-10-10'

    """

    description_string = (
        "GetFx {}: Copyright (c) 2021-2022".format(getfx.__version__)
        + " Kamil Niklasinski\nProgram to display currency exchange rate."
    )

    epilog_string = "Please note this program comes without any warranty!"

    parser = ap.ArgumentParser(
        description=description_string,
        formatter_class=ap.RawTextHelpFormatter,
        epilog=epilog_string,
    )
    parser.add_argument(
        "currency",
        metavar="CCY",
        type=str,
        nargs="?",
        default=DEFAULT_CURRENCY,
        help="Currency to get average NBP FX rate",
    )
    parser.add_argument(
        "-d", "--date", help="effective currency exchange date"
    )

    return parser.parse_args(test_args)
