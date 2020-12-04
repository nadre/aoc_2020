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
    # day_3()
    day_4()


def day_4():
    logger.info('~~~ day 4 ~~~')
    passports = inputs.get_passports('4')
    print(sum([1 for pp in passports if pp.is_valid()]))
    print(sum([1 for pp in passports if pp.is_valid2()]))


def day_3():
    logger.info('~~~ day 3 ~~~')
    tree_map = inputs.get_tree_map('3')
    max_x = len(tree_map[0]) - 1
    max_y = len(tree_map) - 1
    tree_counts = []
    for step_size_x, step_size_y in [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]:
        tree_count = 0
        pos_x = 0
        pos_y = 0

        while pos_y < max_y:
            pos_x = (pos_x + step_size_x) % (max_x + 1)
            pos_y = min(pos_y + step_size_y, max_y)
            val = tree_map[pos_y][pos_x]

            if val == '#':
                tree_count += 1

        print(step_size_x, step_size_y, tree_count)
        tree_counts.append(tree_count)

    print(np.prod(tree_counts))


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
