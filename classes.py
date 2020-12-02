#!/usr/bin/env python3

import re


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
