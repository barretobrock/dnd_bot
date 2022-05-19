#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tools for describing a player character."""
from random import (
    choice,
    randrange
)
from typing import (
    Dict,
    List
)
from slacktools.block_kit import BlockKitBuilder as BKitB
from dnd.core.abilities import Ability, Constitution
from dnd.core.dice import stats_roll
from dnd.core.races import (
    NAME_LIST,
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
    char_class = 'Nothing'
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
            self.name = choice(NAME_LIST).title()
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

    def info_blocks(self) -> List[Dict]:
        """Returns character info as BlockKit blocks"""
        return [
            BKitB.make_block_section(f'*`{self.name}`*: `{self.char_class}` `{self._race.race}`'),
            BKitB.make_block_divider(),
            BKitB.make_block_section(f'HP: *`{self.current_hp}`*/`{self.max_hp}` XP: `{self.xp}`'),
            BKitB.make_context_section(elements=[
                getattr(self, x).__repr__() for x in ['strength', 'dexterity', 'constitution',
                                                      'intelligence', 'wisdom', 'charisma']
            ])
        ]

    def __repr__(self):
        return """
        `{name}`: `{char_class}` `{race}` 
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
    char_class = 'Barbarian'
    hit_die = 12

    def __init__(self, owner, name, **attrs):
        super().__init__(owner, name, **attrs)


class Bard(Character):
    char_class = 'Bard'
    hit_die = 8

    def __init__(self, owner, name, **attrs):
        super().__init__(owner, name, **attrs)


class Cleric(Character):
    char_class = 'Cleric'
    hit_die = 8

    def __init__(self, owner, name, **attrs):
        attrs.update({
            'char_class': 'Cleric',
            'hit_die': 8,
        })
        super().__init__(owner, name, **attrs)


class Druid(Character):
    char_class = 'Druid'
    hit_die = 8

    def __init__(self, owner, name, **attrs):
        super().__init__(owner, name, **attrs)


class Fighter(Character):
    char_class = 'Fighter'
    hit_die = 10

    def __init__(self, owner, name, **attrs):
        super().__init__(owner, name, **attrs)


class Monk(Character):
    char_class = 'Monk'
    hit_die = 8

    def __init__(self, owner, name, **attrs):
        super().__init__(owner, name, **attrs)


class Paladin(Character):
    char_class = 'Paladin'
    hit_die = 10

    def __init__(self, owner, name, **attrs):
        super().__init__(owner, name, **attrs)


class Ranger(Character):
    char_class = 'Ranger'
    hit_die = 10

    def __init__(self, owner, name, **attrs):
        super().__init__(owner, name, **attrs)


class Rogue(Character):
    char_class = 'Rogue'
    hit_die = 8

    def __init__(self, owner, name, **attrs):
        super().__init__(owner, name, **attrs)


class Sorcerer(Character):
    char_class = 'Sorcerer'
    hit_die = 6

    def __init__(self, owner, name, **attrs):
        super().__init__(owner, name, **attrs)


class Warlock(Character):
    char_class = 'Warlock'
    hit_die = 8

    def __init__(self, owner, name, **attrs):
        super().__init__(owner, name, **attrs)


class Wizard(Character):
    char_class = 'Wizard'
    hit_die = 6

    def __init__(self, owner, name, **attrs):
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
    Sorcerer,
    Warlock,
    Wizard
]
