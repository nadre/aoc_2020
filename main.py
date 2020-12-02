#!/usr/bin/env python3
"""
2020 AOC Golfing
"""

__author__ = "Erdan Genc"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import logging
import inputs
import itertools
import numpy as np


def main(args):
    # day_1()
    # day_2()
    day_3()


def day_3():
    logger.info('~~~ day 3 ~~~')


def day_2():
    logger.info('~~~ day 2 ~~~')
    passwords = inputs.get_passwords_with_policy('2')
    print(sum([1 for pw in passwords if pw.is_valid()]))
    print(sum([1 for pw in passwords if pw.is_valid2()]))


def day_1():
    logger.info('~~~ day 1 ~~~')
    numbers_set = inputs.get_input_as_int_set('1')
    [print(comb, np.prod(comb)) for comb in itertools.combinations(numbers_set, r=2) if sum(comb) == 2020]
    [print(comb, np.prod(comb)) for comb in itertools.combinations(numbers_set, r=3) if sum(comb) == 2020]


if __name__ == "__main__":
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    # parser.add_argument("arg", help="Required positional argument")

    # Optional argument flag which defaults to False
    parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-n", "--name", action="store", dest="name")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
