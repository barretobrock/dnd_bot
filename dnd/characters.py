#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tools for describing a player character."""


class Character:
    """Basic characteristics for character"""
    level = 1
    xp = 0

    def __init__(self, name, _class, **attrs):
        self.name = name
        self.char_class = _class
        # self.charisma = attrs.pop('charisma', 0)

    def get_attributes(self):
        """Get all character attributes"""
        attr_dict = {}
        for k in dir(self):
            val = self.__getattribute__(k)
            if any([not k.startswith('__'), not callable(val)]):
                attr_dict.update({k: val})
        return attr_dict


class Race:
    """Basic characteristics for race"""
    def __init__(self):
        pass


class Barbarian(Character):
    def __init__(self, name, **attrs):
        attrs.update({
            '_class': ['Barbarian'],
            'name': name
        })
        super().__init__(**attrs)


class Bard(Character):
    def __init__(self, name, **attrs):
        attrs.update({
            '_class': ['Bard'],
            'name': name,
        })
        super().__init__(**attrs)


class Cleric(Character):
    def __init__(self, name, **attrs):
        attrs.update({
            '_class': ['Cleric'],
            'name': name
        })
        super().__init__(**attrs)


class Druid(Character):
    def __init__(self, name, **attrs):
        attrs.update({
            '_class': ['Druid'],
            'name': name
        })
        super().__init__(**attrs)


class Fighter(Character):
    def __init__(self, name, **attrs):
        attrs.update({
            '_class': ['Fighter'],
            'name': name
        })
        super().__init__(**attrs)


class Monk(Character):
    def __init__(self, name, **attrs):
        attrs.update({
            '_class': ['Monk'],
            'name': name
        })
        super().__init__(**attrs)


class Paladin(Character):
    def __init__(self, name, **attrs):
        attrs.update({
            '_class': ['Paladin'],
            'name': name
        })
        super().__init__(**attrs)


class Ranger(Character):
    def __init__(self, name, **attrs):
        attrs.update({
            '_class': ['Ranger'],
            'name': name
        })
        super().__init__(**attrs)


class Rogue(Character):
    def __init__(self, name, **attrs):
        attrs.update({
            '_class': ['Rogue'],
            'name': name
        })
        super().__init__(**attrs)


class Sorceror(Character):
    def __init__(self, name, **attrs):
        attrs.update({
            '_class': ['Sorceror'],
            'name': name
        })
        super().__init__(**attrs)


class Warlock(Character):
    def __init__(self, name, **attrs):
        attrs.update({
            '_class': ['Warlock'],
            'name': name
        })
        super().__init__(**attrs)


class Wizard(Character):
    def __init__(self, name, **attrs):
        attrs.update({
            '_class': ['Wizard'],
            'name': name
        })
        super().__init__(**attrs)
