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
from collections import Counter


def main(args):
    # day_1()
    # day_2()
    # day_3()
    # day_4()
    # day_5()
    # day_6()
    # day_7()
    # day_8()
    # day_9()
    # day_10()
    # day_11_1()
    # day_11_2()
    # day_13_1()
    day_13_2()


def day_11_2():
    logger.info('~~~ day 11 part 2~~~')
    seats = inputs.get_input_as_list('11')
    seats = [[c for c in s] for s in seats]
    seats = np.array(seats)

    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1),
    ]

    change = True
    while change:
        change = False
        seat_status = {}
        for x in range(0, seats.shape[0]):
            for y in range(0, seats.shape[1]):

                val = seats[x, y]
                if val == '.':
                    continue

                seen_seats = []
                for x_, y_ in directions:
                    i = x + x_
                    j = y + y_
                    while 0 <= i < seats.shape[0] and 0 <= j < seats.shape[1]:
                        seat = seats[i, j]
                        if seat == '#' or seat == 'L':
                            seen_seats.append(seat)
                            break
                        i += x_
                        j += y_
                c = Counter(seen_seats)
                seat_status[(x, y)] = val, c['#']

        for (x, y), (val, taken_seats) in seat_status.items():
            if val == 'L' and taken_seats == 0:
                seats[x, y] = '#'
                change = True
            elif val == '#' and taken_seats >= 5:
                seats[x, y] = 'L'
                change = True

        print('\n'.join(''.join(s) for s in seats).count('#'))


def day_11_1():
    logger.info('~~~ day 11 ~~~')
    seats = inputs.get_input_as_list('11')
    seats = [[c for c in s] for s in seats]
    seats = np.array(seats)
    seats = np.pad(seats, [(1, 1), (1, 1)])
    seats = np.where(seats == '.', 0, seats)

    change = True
    while change:
        change = False
        seat_status = {}
        for x in range(1, seats.shape[0] - 1):
            for y in range(1, seats.shape[1] - 1):
                nb = np.copy(seats[x - 1:x + 2, y - 1:y + 2])
                nb[1, 1] = 'X'
                nb = nb.flatten()
                val = seats[x, y]
                c = Counter(nb)
                seat_status[(x, y)] = val, c['#']

        for (x, y), (val, taken_seats) in seat_status.items():
            if val == 'L' and taken_seats == 0:
                seats[x, y] = '#'
                change = True
            elif val == '#' and taken_seats >= 4:
                seats[x, y] = 'L'
                change = True

        print('\n'.join(''.join(s) for s in seats).count('#'))


def day_13_1():
    logger.info('~~~ day 13 part 1 ~~~')
    timestamp, bus_ids = inputs.get_input_as_list('13')
    timestamp = int(timestamp)
    bus_ids = [int(bid) for bid in bus_ids.split(',') if bid != 'x']
    bus_numbers = {bid - timestamp % bid: bid for bid in bus_ids}
    min_d = min(bus_numbers.keys())
    print(min_d * bus_numbers[min_d])


def day_13_2():
    logger.info('~~~ day 13 part 2 ~~~')
    _, bus_ids = inputs.get_input_as_list('13')
    bus_numbers = {i: int(bid) for i, bid in enumerate(bus_ids.split(',')) if bid != 'x'}
    timestamp = 1
    prod = 1
    for i, (time_diff, bid) in enumerate(bus_numbers.items()):
        while (timestamp + time_diff) % bid != 0:
            timestamp += prod
        prod *= bid
    print(timestamp)


def day_10():
    logger.info('~~~ day 10 part 2 ~~~')
    ab = inputs.get_adapter_bag('10')
    print(ab.get_answer1())
    print(ab.get_answer2())


def day_9():
    logger.info('~~~ day 9 ~~~')
    xms_system = inputs.get_xms_system('9', 25)
    # xms_system = inputs.get_xms_system('9-test', 5)
    invalid_number = xms_system.get_invalid_number()
    print(invalid_number)
    r = xms_system.get_range(invalid_number)
    print(sum([min(r), max(r)]))


def day_8():
    logger.info('~~~ day 8 ~~~')
    instruction_set = inputs.get_instruction_set('8')
    print(instruction_set.run_and_repair())


def day_7():
    logger.info('~~~ day 7 ~~~')
    bag_rules = inputs.get_bag_rules('7')
    print(bag_rules.get_inverse_count('shiny gold'))
    print(bag_rules.get_count('shiny gold') - 1)


def day_6():
    logger.info('~~~ day 6 ~~~')
    forms = inputs.get_forms('6')
    print(sum([len(f.question_answered_yes) for f in forms]))
    forms = inputs.get_forms2('6')
    print(sum([f.get_counts() for f in forms]))


def day_5():
    logger.info('~~~ day 5 ~~~')
    boarding_passes = inputs.get_boarding_passes('5')
    ids = [bp.id for bp in boarding_passes]
    ids.sort()
    print(max(ids))
    for i, id_ in enumerate(ids[:-1]):
        if id_ + 1 != ids[i + 1]:
            print(id_ + 1)


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
