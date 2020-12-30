#!/usr/bin/env python3

import re
import itertools
from Powerset import powerset


class MemoryMap2:
    def __init__(self, memory_map_str: str):
        self.memory_map_lines = memory_map_str.split('\n')
        self.mask = {i: val for i, val in enumerate(self.memory_map_lines[0][::-1]) if val != '0'}
        self.values = [self.get_value(line) for line in self.memory_map_lines[1:]]

    def get_all_masked_addresses(self, address):
        masked_address = self.get_masked_adress(address, self.mask)
        zero_address = [v if v != 'X' else '0' for v in masked_address]
        floating_bits = [i for i, v in enumerate(masked_address) if v == 'X']
        for subset in powerset(floating_bits):
            new_mask = zero_address.copy()
            for i in subset:
                new_mask[i] = '1'
            a = ''.join(new_mask)
            b = int(a, 2)
            yield b

    def get_all_addresses_with_values(self):
        result = {}
        for address, value in self.values:
            for masked_address in self.get_all_masked_addresses(address):
                result[masked_address] = value
        return result

    @staticmethod
    def get_value(line):
        address, value = line.split(' = ')
        value = int(value)
        address = int(re.findall('\\d+', address)[0])
        return address, value

    @staticmethod
    def get_masked_adress(address, mask):
        new_address = list(format(int(address), '036b'))
        new_address.reverse()
        for i, val in mask.items():
            new_address[i] = str(val)
        new_address.reverse()
        return new_address


class MemoryMap:
    def __init__(self, memory_map_str: str):
        self.memory_map_lines = memory_map_str.split('\n')
        self.mask = {i: val for i, val in enumerate(self.memory_map_lines[0][::-1]) if val != 'X'}
        self.values = [self.get_value(line) for line in self.memory_map_lines[1:]]

    @staticmethod
    def get_value(line):
        address, value = line.split(' = ')
        value = format(int(value), '036b')
        address = int(re.findall('\\d+', address)[0])
        return address, value

    def get_saved_values(self):
        saved_values = {}
        for address, value in self.values:
            new_value = list(value)
            new_value.reverse()
            for i, val in self.mask.items():
                new_value[i] = val
            new_value.reverse()
            saved_values[address] = int(''.join(new_value), 2)
        return saved_values


class AdapterBag:
    def __init__(self, int_set: set):
        self.adapters = int_set
        self.adapters_sorted = list(int_set)
        self.adapters_sorted.sort()

    def get_answer1(self):
        jumps = [3]
        tmp_adapters = [0] + self.adapters_sorted
        for i, adapter in enumerate(tmp_adapters):
            if i + 1 == len(tmp_adapters):
                break
            jumps.append(tmp_adapters[i + 1] - adapter)
        return jumps.count(1) * jumps.count(3)

    def get_answer2(self):
        tmp_adapters = [0] + self.adapters_sorted
        num_paths = [0] * len(tmp_adapters)
        num_paths[0] = 1
        for i, adapter in enumerate(tmp_adapters):
            j = i - 1
            while j >= 0 and adapter - tmp_adapters[j] <= 3:
                num_paths[i] += num_paths[j]
                j -= 1
        return num_paths[-1]


def pairwise(iterable):
    it = iter(iterable)
    a = next(it, None)

    for b in it:
        yield a, b
        a = b


class XMASSystem:
    def __init__(self, numbers, preamble_length):
        self.numbers = numbers
        self.preamble_length = preamble_length
        self.position = 0

    def get_valid_numbers(self):
        preamble_numbers = self.numbers[self.position:self.position + self.preamble_length]
        return [sum(x) for x in itertools.combinations(preamble_numbers, 2)]

    def get_invalid_number(self):
        while True:
            current_number = self.numbers[self.preamble_length + self.position]
            if current_number in self.get_valid_numbers():
                self.position += 1
            else:
                return current_number

    def get_range(self, expected_sum):
        for range_length in range(2, len(self.numbers) - 1):
            for pos in range(len(self.numbers)):
                current_sum = sum(self.numbers[pos:pos + range_length])
                if current_sum == expected_sum:
                    return self.numbers[pos:pos + range_length]


class InstructionSet:
    def __init__(self, instructions_str):
        self.instructions_str = instructions_str

        self.instructions = []
        self.visited_positions = []
        self.current_pos = 0
        self.accumulator = 0

        self.repair_pos = 0
        for line in instructions_str:
            op, arg = line.split()
            self.instructions.append((op, int(arg)))
        self.num_instructions = len(self.instructions)
        self.original_instructions = [l for l in self.instructions]

    def run(self):
        while True:
            if self.current_pos in self.visited_positions:
                return False
            if self.current_pos == self.num_instructions:
                return self.accumulator
            self.step()

    def run_and_repair(self):
        terminated = False
        while not terminated:
            terminated = self.run()
            self.repair_step()

        return terminated

    def repair_step(self):
        self.instructions = [l for l in self.original_instructions]
        self.visited_positions = []
        self.current_pos = 0
        self.accumulator = 0
        op, arg = self.instructions[self.repair_pos]
        if op == 'nop':
            op = 'jmp'
        elif op == 'jmp':
            op = 'nop'
        self.instructions[self.repair_pos] = (op, arg)
        # print(self.repair_pos, self.num_instructions)
        self.repair_pos += 1

    def step(self):
        self.visited_positions.append(self.current_pos)
        op, arg = self.instructions[self.current_pos]

        if op == 'nop':
            self.current_pos += 1
            return
        elif op == 'acc':
            self.accumulator += arg
            self.current_pos += 1
            return
        elif op == 'jmp':
            self.current_pos += arg
            return


class BagRules:
    def __init__(self, rules):
        self.rules = rules
        self.map = {}
        self.inverse_map = {}
        for line in self.rules.split('\n'):
            key, values = line.split(' contain ')
            key_bag_type = key.rstrip('.').rstrip('bag').rstrip('bags').rstrip(' ')

            if values == 'no other bags.':
                self.map[key_bag_type] = [('X', 1)]
                continue

            for val in values.split(', '):
                val_bag = val.rstrip('.').rstrip('bag').rstrip('bags').rstrip(' ')
                bag_values = val_bag.split()
                num_bags = int(bag_values[0])
                bag_type = ' '.join(bag_values[1:])

                if bag_type in self.inverse_map:
                    self.inverse_map[bag_type].append(key_bag_type)
                else:
                    self.inverse_map[bag_type] = [key_bag_type]

                if key_bag_type in self.map:
                    self.map[key_bag_type].append((bag_type, num_bags))
                else:
                    self.map[key_bag_type] = [(bag_type, num_bags)]

    def get_count(self, key):
        count = 1
        for node, value in self.map[key]:
            if node != 'X':
                count += value * self.get_count(node)
        return count

    def get_inverse_count(self, key):
        bags_that_can_contain = set(self.inverse_map[key])

        while True:
            new_bags = set()
            for bag_type in bags_that_can_contain:
                if bag_type not in self.inverse_map:
                    continue
                for new_bag_type in self.inverse_map[bag_type]:
                    if new_bag_type in bags_that_can_contain:
                        continue
                    else:
                        new_bags.add(new_bag_type)

            if len(new_bags) == 0:
                break
            else:
                bags_that_can_contain = bags_that_can_contain.union(new_bags)

        return len(bags_that_can_contain)


class Form:
    def __init__(self, form_string):
        self.question_answered_yes = set()
        for line in form_string.split('\n'):
            for char in line.strip():
                self.question_answered_yes.add(char)


class Form2:
    def __init__(self, form_string):
        self.question_answered_yes = {}
        self.count = 0
        for line in form_string.split('\n'):
            self.count += 1
            for char in line.strip():
                count = 1
                if char not in self.question_answered_yes:
                    pass
                else:
                    count += self.question_answered_yes[char]
                self.question_answered_yes[char] = count

    def get_counts(self):
        counts = 0
        for value in self.question_answered_yes.values():
            if value == self.count:
                counts += 1
        return counts


class BoardingPass:
    def __init__(self, code):
        self.code = code
        self._set_row()
        self._set_col()
        self._set_id()

    def _set_row(self):
        self.row_code = self.code[:-3] \
            .replace('F', '0') \
            .replace('B', '1')

        self.row = int(self.row_code, 2)

    def _set_col(self):
        self.col_code = self.code[-3:] \
            .replace('R', '1') \
            .replace('L', '0')

        self.col = int(self.col_code, 2)

    def _set_id(self):
        self.id = self.row * 8 + self.col


class PasswordPolicy:
    def __init__(self, min_, max_, char):
        self.min = int(min_)
        self.max = int(max_)
        self.char = char


class Password:
    def __init__(self, line):
        range_, char, value = line.split()
        self.value = value
        min_, max_ = range_.split('-')
        policy = PasswordPolicy(min_, max_, char[0])
        self.policy = policy

    def is_valid(self):
        char_frequency = self.value.count(self.policy.char)
        return self.policy.min <= char_frequency <= self.policy.max

    def is_valid2(self):
        positions = [pos.start() + 1 for pos in re.finditer(self.policy.char, self.value)]
        count = 0
        if self.policy.min in positions:
            count += 1
        if self.policy.max in positions:
            count += 1
        return count == 1


class Passport:
    def __init__(self, information_string):
        self.required_fields = ['ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt']  # 'cid'
        self.valid_eye_colors = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
        self.information = {}
        for line in information_string.split('\n'):
            for pair_ in line.split():
                x = pair_.split(':')
                if len(x) != 2:
                    continue
                else:
                    self.information[x[0].strip()] = x[1].strip()

    def is_valid(self):
        for field in self.required_fields:
            if field not in self.information:
                return False
        return True

    def is_valid2(self):
        if not self.is_valid():
            return False

        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        byr_ = self.information['byr']
        if 1920 <= int(byr_) <= 2002:
            pass
        else:
            return False

        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        iyr_ = self.information['iyr']
        if 2010 <= int(iyr_) <= 2020:
            pass
        else:
            return False

        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        eyr_ = self.information['eyr']
        if 2020 <= int(eyr_) <= 2030:
            pass
        else:
            return False

        # hgt (Height) - a number followed by either cm or in:
        hgt = self.information['hgt']
        if hgt.endswith('cm'):
            hgt = int(hgt[:-2])
            # If cm, the number must be at least 150 and at most 193.
            if 150 <= hgt <= 193:
                pass
            else:
                return False
        elif hgt.endswith('in'):
            hgt = int(hgt[:-2])
            # If in, the number must be at least 59 and at most 76.
            if 59 <= hgt <= 76:
                pass
            else:
                return False
        else:
            return False

        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        hcl = self.information['hcl']
        if not hcl.startswith('#'):
            return False
        hcl = hcl[1:]
        if len(hcl) != 6:
            return False
        if not hcl.isalnum():
            return False

        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        ecl = self.information['ecl']
        if ecl in self.valid_eye_colors:
            pass
        else:
            return False

        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        pid = self.information['pid']
        if len(pid) != 9:
            return False
        if not pid.isdigit():
            return False

        return True
