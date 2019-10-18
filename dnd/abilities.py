#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math


class Modifier:
    def __init__(self, value):
        self.value = self.calc_modifier(value)

    def calc_modifier(self, value):
        """Updates the ability's modifier"""
        return math.floor((value - 10) / 2)

    def __repr__(self):
        return '({:+})'.format(self.value)


class Ability:
    """"""
    def __init__(self, value, ability):
        self.name = ability
        self.value = value
        self.modifier = Modifier(value)
        self.mod = self.modifier.value

    def increment_value(self, new_val):
        """Updates the ability's value"""
        self.value += new_val
        self.modifier.calc_modifier(self.value)

    def __repr__(self):
        return '{}: {} {}'.format(self.name.title(), self.value, self.modifier.__repr__())


class Strength(Ability):
    """"""
    def __init__(self, value):
        super().__init__(value, ability='str')


class Dexterity(Ability):
    """"""
    def __init__(self, value):
        super().__init__(value, ability='dex')


class Constitution(Ability):
    """"""
    def __init__(self, value):
        super().__init__(value, ability='con')


class Intelligence(Ability):
    """"""
    def __init__(self, value):
        super().__init__(value, ability='int')


class Wisdom(Ability):
    """"""
    def __init__(self, value):
        super().__init__(value, ability='wis')


class Charisma(Ability):
    """"""
    def __init__(self, value):
        super().__init__(value, ability='cha')

