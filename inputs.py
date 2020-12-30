#!/usr/bin/env python3

from classes import Password, Passport, BoardingPass, Form, Form2, BagRules, \
    InstructionSet, XMASSystem, AdapterBag, MemoryMap, MemoryMap2


def get_memory_maps2(day: str):
    filename = f'inputs/{day}.txt'
    return [MemoryMap2(mm.strip()) for mm in open(filename).read().split('mask = ') if len(mm) > 0]


def get_memory_maps(day: str):
    filename = f'inputs/{day}.txt'
    return [MemoryMap(mm.strip()) for mm in open(filename).read().split('mask = ') if len(mm) > 0]


def get_adapter_bag(day: str):
    return AdapterBag(get_input_as_int_set(day))


def get_bag_rules(day: str):
    filename = f'inputs/{day}.txt'
    return BagRules(open(filename).read())


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


def get_boarding_passes(day: str):
    filename = f'inputs/{day}.txt'
    return [BoardingPass(code) for code in open(filename).read().split('\n')]


def get_forms(day: str):
    filename = f'inputs/{day}.txt'
    return [Form(info) for info in open(filename).read().split('\n\n')]


def get_forms2(day: str):
    filename = f'inputs/{day}.txt'
    return [Form2(info) for info in open(filename).read().split('\n\n')]


def get_instruction_set(day: str):
    filename = f'inputs/{day}.txt'
    return InstructionSet(open(filename).read().split('\n'))


def get_xms_system(day: str, preamble_length: int):
    return XMASSystem(get_input_as_int_list(day), preamble_length)
