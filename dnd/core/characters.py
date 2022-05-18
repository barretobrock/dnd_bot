#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tools for describing a player character."""
from random import randrange
from dnd.core.abilities import Ability, Constitution
from dnd.core.dice import stats_roll
from dnd.core.races import (
    Race,
    race_list
)


def random_char_gen(owner, name=None):
    """Randomly generate a character"""
    rand_char_class = character_classes[randrange(0, len(character_classes) - 1)]
    rand_race = race_list[randrange(0, len(race_list) - 1)]

    return rand_char_class(owner, name=name, race=rand_race)


class Character:
    """Basic characteristics for character"""
    level = 1
    xp = 0
    hit_die = 8  # Default is d8
    constitution = Constitution(0)

    def __init__(self, owner_hash: str, name: str = None, race: Race = None, **attrs):
        # User's Slack ID
        self.owner_hash = owner_hash
        if race is None:
            self._race = Race()
        else:
            self._race = race
        if name is None:
            # Randomly generate a name based on character's race
            self.name = self._race.name_list[randrange(0, len(self._race.name_list) - 1)].title()
        else:
            self.name = name.title()
        self.name_lower = self.name.lower()

        for k, v in attrs.items():
            self.__setattr__(k, v)
        abilities = [x['ability'] for x in stats_roll()]
        # Set attributes
        ability: Ability
        for ability in abilities:
            self.__setattr__(ability.name, ability)
        # Set max hp
        self.max_hp = self.hit_die + self.constitution.value

        # Set race bonuses
        for k, v in self._race.__dict__.items():
            if 'bonus' in k:
                # Ability or HP bonus
                prefix = k.split('_')[0]
                if prefix == 'hp':
                    self.update_ability('max_hp', v)
                else:
                    self.update_ability(prefix, v)
            else:
                self.__setattr__(k, v)

        self.current_hp = self.max_hp

    def get_attributes(self):
        """Get all character attributes & exports to dict"""
        attr_dict = {}
        for k in dir(self):
            val = self.__getattribute__(k)
            if any([not k.startswith('__'), not callable(val)]):
                attr_dict.update({k: val})
        return attr_dict

    def update_ability(self, ability, increment_value):
        """Updates ability or hp by increment_value"""
        ability_obj = self.__getattribute__(ability)
        if isinstance(ability_obj, int):
            ability_obj += increment_value
        else:
            ability_obj.value += increment_value
        self.__setattr__(ability, ability_obj)

    def __repr__(self):
        return """
        `{name}`: `{race}` `{char_class}`
        ----------------------------------------
        HP: `{current_hp}/{max_hp}` XP: `{xp}` 
        {strength}
        {dexterity}
        {constitution}
        {intelligence}
        {wisdom}
        {charisma}
        """.format(**self.get_attributes())


class Barbarian(Character):
    def __init__(self, owner, name, **attrs):
        attrs.update({
            'char_class': 'Barbarian',
            'hit_die': 12,
        })
        super().__init__(owner, name, **attrs)


class Bard(Character):
    def __init__(self, owner, name, **attrs):
        attrs.update({
            'char_class': 'Bard',
            'hit_die': 8,
        })
        super().__init__(owner, name, **attrs)


class Cleric(Character):
    def __init__(self, owner, name, **attrs):
        attrs.update({
            'char_class': 'Cleric',
            'hit_die': 8,
        })
        super().__init__(owner, name, **attrs)


class Druid(Character):
    def __init__(self, owner, name, **attrs):
        attrs.update({
            'char_class': 'Druid',
            'hit_die': 8,
        })
        super().__init__(owner, name, **attrs)


class Fighter(Character):
    def __init__(self, owner, name, **attrs):
        attrs.update({
            'char_class': 'Fighter',
            'hit_die': 10,
        })
        super().__init__(owner, name, **attrs)


class Monk(Character):
    def __init__(self, owner, name, **attrs):
        attrs.update({
            'char_class': 'Monk',
            'hit_die': 8,
        })
        super().__init__(owner, name, **attrs)


class Paladin(Character):
    def __init__(self, owner, name, **attrs):
        attrs.update({
            'char_class': 'Paladin',
            'hit_die': 10,
        })
        super().__init__(owner, name, **attrs)


class Ranger(Character):
    def __init__(self, owner, name, **attrs):
        attrs.update({
            'char_class': 'Ranger',
            'hit_die': 10,
        })
        super().__init__(owner, name, **attrs)


class Rogue(Character):
    def __init__(self, owner, name, **attrs):
        attrs.update({
            'char_class': 'Rogue',
            'hit_die': 8,
        })
        super().__init__(owner, name, **attrs)


class Sorceror(Character):
    def __init__(self, owner, name, **attrs):
        attrs.update({
            'char_class': 'Sorceror',
            'hit_die': 6,
        })
        super().__init__(owner, name, **attrs)


class Warlock(Character):
    def __init__(self, owner, name, **attrs):
        attrs.update({
            'char_class': 'Warlock',
            'hit_die': 8,
        })
        super().__init__(owner, name, **attrs)


class Wizard(Character):
    def __init__(self, owner, name, **attrs):
        attrs.update({
            'char_class': 'Wizard',
            'hit_die': 6,
        })
        super().__init__(owner, name, **attrs)


character_classes = [
    Barbarian,
    Bard,
    Cleric,
    Druid,
    Fighter,
    Monk,
    Paladin,
    Ranger,
    Rogue,
    Sorceror,
    Warlock,
    Wizard
]
