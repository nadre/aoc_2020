#!/usr/bin/env python3

import re

class PasswordPolicy:
    def __init__(self, min, max, char):
        self.min = int(min)
        self.max = int(max)
        self.char = char

class Password:
    def __init__(self, line):
        range, char, value = line.split()
        self.value = value
        min, max = range.split('-')
        policy = PasswordPolicy(min, max, char[0])
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