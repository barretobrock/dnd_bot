#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import random
from collections import namedtuple
from dnd.utils import eval_expr
from dnd.abilities import Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma


try:
    # Use the system PRNG if possible
    rnd = random.SystemRandom()
except NotImplementedError:
    import warnings
    # Mersenne twister is the default Python PRNG
    warnings.warn("A secure pseudo-random number generator is not available "
                  "on your system. Falling back to Mersenne Twister.")
    rnd = random


def read_dice_str(input_txt):
    """
    Interpret a D&D dice string, eg. 3d10.
    """

    dice_re = re.compile(r'(\d)*d(\d+)', flags=re.I)
    Dice = namedtuple('Dice', ('rolls', 'sides'))
    # Limit to the number of rolls/sides in one go.
    limit = 10000
    matches = []
    for found in dice_re.finditer(input_txt):
        rolls = int(found.group(1)) if found.group(1) is not None else 1
        sides = int(found.group(2))
        if rolls > limit or sides > limit:
            raise ValueError("Number of dice rolls or sides exceeded limit.")
        matches.append({
            'match': found.group(),
            'dice': Dice(*[rolls, sides])
        })

    return matches


def roll_dice(input_txt, str_output=False):
    """Rolls a dice"""

    rolls = []
    for m in read_dice_str(input_txt):
        dice = m['dice']
        roll_total = 0
        for r in range(dice.rolls):
            roll = rnd.randrange(1, m['dice'].sides + 1)
            roll_total += roll
            rolls.append("{}/{}".format(roll, m['dice'].sides))
        input_txt = input_txt.replace(m['match'], '{}'.format(roll_total))

    # Once we're done rolling all the dice, put it all together
    # Input str should have all dice rolls done, so now eval into a number
    result = eval_expr(input_txt)

    if str_output:
        return '`{}`: {}'.format(result, ' '.join(rolls))

    return result, rolls


def stats_roll():
    """Takes no input and returns the results for a DnD 5e stats roll (4d6 drop lowest)"""
    stat_rolls = []
    abilities = [Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma]
    for ability in abilities:
        total, rolls = roll_dice("4d6")
        lowest = int(min(rolls).split("/")[0])
        total -= lowest
        stat_rolls.append({'ability': ability(total), 'rolls': ', '.join(rolls)})

    return stat_rolls


def dir_roll():
    """Roll direction"""
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'Stay']
    dir_rolls = '{}'.format(rnd.choice(dirs))

    return dir_rolls

