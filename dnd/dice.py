#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import random
from collections import namedtuple


try:
    # Use the system PRNG if possible
    random = random.SystemRandom()
except NotImplementedError:
    import warnings
    # Mersenne twister is the default Python PRNG
    warnings.warn("A secure pseudo-random number generator is not available "
                  "on your system. Falling back to Mersenne Twister.")


dice_re = re.compile(r'(\d+)d(\d+)', flags=re.I)
Dice = namedtuple('Dice', ('num', 'faces'))


def read_dice_str(dice_str):
    """Interpret a D&D dice string, eg. 3d10.

    Returns
    -------
    dice : tuple
      A named tuple with the scheme (num, faces), so '3d10' return
      (num=3, faces=10)

    """
    match = dice_re.match(dice_str)
    if match is None:
        raise ValueError("Cannot interpret dice string {}".format(dice_str))
    dice = Dice(num=int(match.group(1)),
                faces=int(match.group(2)))
    return dice


def stats_roll():
    """Takes no input and returns the results for a DnD 5e stats roll (4d6 drop lowest)"""
    stat_rolls = ''
    for i in range(6):
        total, rolls = dice_roller("4d6")
        lowest = int(min(rolls).split("/")[0])
        total = int(total) - lowest
        stat_rolls = stat_rolls + str(total) + str(rolls) + "\n"

    return stat_rolls


def dir_roll():
    """Roll direction"""
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'Stay']
    dir_rolls = str(random.choice(dirs))

    return dir_rolls


def dice_roller(input_text):
    """Takes in a string with dice and returns the rolled dice and the sum"""
    # Function Variables
    # Regex for detecting dice notation
    r_dice = re.compile(r'\d*d\d+')
    # List for keeping track of the rolls
    rolls = []

    def roll_dice(d):
        """Dice rolling code"""
        result = 0
        # Zeroth group of regex match is the match itself
        dice = d.group(0)

        # Split the string at the letter d
        dice_split = dice.split("d")

        # Read the number of rolls, fall back to one
        times = int(dice_split[0]) if dice_split[0] is not '' else 1
        sides = int(dice_split[1])

        # Actually rolling the dice
        for t in range(times):
            roll = random.randrange(1, sides+1)
            rolls.append(str(roll) + "/" + str(sides))
            result += roll

        return str(result)

    # Regex the input and automatically run the dice rolling code
    #   when dice notation is detected and evaluate the output
    output = eval(r_dice.sub(roll_dice, input_text))

    return output, rolls
