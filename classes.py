#!/usr/bin/env python3

import re


class BoardingPass:
    def __init__(self, code):
        self.code = code
        self._set_row()
        self._set_col()
        self._set_id()

    def _set_row(self):
        self.row_code = self.code[:-3]\
            .replace('F', '0')\
            .replace('B', '1')

        self.row = int(self.row_code, 2)

    def _set_col(self):
        self.col_code = self.code[-3:]\
            .replace('R', '1')\
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
