#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .bot import DNDBot
from .abilities import Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma
from .utils import eval_expr


from ._version import get_versions
__version__ = get_versions()['version']
__update_date__ = get_versions()['date']
del get_versions
