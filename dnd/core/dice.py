#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from typing import (
    Dict,
    List,
    Union
)
from d20 import (
    roll,
    RollResult,
    RollSyntaxError
)
from dnd.core.abilities import (
    Charisma,
    Constitution,
    Dexterity,
    Intelligence,
    Strength,
    Wisdom
)


try:
    # Use the system PRNG if possible
    rnd = random.SystemRandom()
except NotImplementedError:
    import warnings
    # Mersenne twister is the default Python PRNG
    warnings.warn("A secure pseudo-random number generator is not available "
                  "on your system. Falling back to Mersenne Twister.")
    rnd = random


def roll_dice(input_txt: str, str_output: bool = False) -> Union[str, RollResult]:
    """Rolls a dice"""
    try:
        roll_result = roll(input_txt)
    except RollSyntaxError:
        return f'Unable to parse for roll: {input_txt}'
    if str_output:
        return roll_result.result
    else:
        return roll_result


def stats_roll() -> List[Dict[str, str]]:
    """Takes no input and returns the results for a DnD 5e stats roll (4d6 drop lowest)"""
    stat_rolls = []
    abilities = [Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma]
    for ability in abilities:
        result = roll_dice('4d6kh3', str_output=False)
        total = result.total
        rolls = [f'{x.number}' for x in result.expr.keptset]
        stat_rolls.append({'ability': ability(total), 'rolls': ', '.join(rolls)})

    return stat_rolls


def dir_roll() -> str:
    """Roll direction"""
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'Stay']
    return rnd.choice(dirs)
