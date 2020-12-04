#!/usr/bin/env python3

from classes import Password, Passport


def get_input_as_list(day: str):
    filename = f'inputs/{day}.txt'
    return [line.strip() for line in open(filename)]


def get_input_as_int_list(day: str):
    filename = f'inputs/{day}.txt'
    return [int(line) for line in open(filename)]


def get_input_as_int_set(day: str):
    return set(get_input_as_int_list(day))


def get_passwords_with_policy(day: str):
    return [Password(line) for line in get_input_as_list(day)]


def get_tree_map(day: str):
    return [list(line.rstrip()) for line in get_input_as_list(day)]


def get_passports(day: str):
    filename = f'inputs/{day}.txt'
    return [Passport(info) for info in open(filename).read().split('\n\n')]
