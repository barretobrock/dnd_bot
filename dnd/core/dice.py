#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import re
from typing import (
    Dict,
    List,
    Union
)
from d20 import (
    Dice,
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

MAX_SIDES = 200
MAX_ROLLS = 100

try:
    # Use the system PRNG if possible
    rnd = random.SystemRandom()
except NotImplementedError:
    import warnings
    # Mersenne twister is the default Python PRNG
    warnings.warn("A secure pseudo-random number generator is not available "
                  "on your system. Falling back to Mersenne Twister.")
    rnd = random


class Dice:
    sides = 0
    rolls = 0

    def __init__(self, msg_part: str):
        result = re.search(r'(\d*)d(\d+)', msg_part)
        if result is not None:
            if result.group(1) == '':
                self.rolls = 1
            else:
                self.rolls = int(result.group(1))
            self.sides = int(result.group(2))


class MaxRollsExceededException(Exception):
    pass


class MaxSidesExceededException(Exception):
    pass


def roll_dice(input_txt: str, str_output: bool = False) -> Union[str, RollResult]:
    """Rolls a dice"""
    # Ensure the rolls are within reason
    dice_used = [Dice(x) for x in input_txt.split(' ')]
    sides_total = sum([x.sides for x in dice_used])
    rolls_total = sum([x.rolls for x in dice_used])
    if sides_total > MAX_SIDES:
        raise MaxSidesExceededException('User exceeded the maximum sides used in a request.')
    elif rolls_total > MAX_ROLLS:
        raise MaxRollsExceededException('User exceeded the maximum rolls used in a request.')
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
