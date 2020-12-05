"""
You can auto-discover and run all tests with this command:

    py.test

Documentation: https://docs.pytest.org/en/latest/
"""

import inputs


def test_day5():
    assert inputs.get_boarding_passes('5-test')[0].row == 102
    assert inputs.get_boarding_passes('5-test')[0].col == 4
    assert inputs.get_boarding_passes('5-test')[0].id == 820


def test_day4_valid():
    passports = inputs.get_passports('4-valid')
    assert sum([1 for pp in passports if pp.is_valid2()]) == 4


def test_day4_invalid():
    passports = inputs.get_passports('4-invalid')
    assert sum([1 for pp in passports if pp.is_valid2()]) == 0

