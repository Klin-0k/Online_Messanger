import pytest


def main_question():
    return 42


def plus(a, b):
    return a + b


def minus(a, b):
    return a - b


def test_main_question():
    assert main_question() == 42


def test_plus():
    assert plus(1, 2) == 3
    assert plus(-1, -2) == -3
    assert plus(0, 0) == 0


def test_minus():
    assert minus(1, 2) == -1
    assert minus(-1, -2) == 1
    assert minus(0, 0) == 0
