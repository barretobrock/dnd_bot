#!/usr/bin/env python3
# -*- coding: utf-8 -*-

NAME_LIST = [
    'Dian', 'Nese', 'Falledrick', 'Mae', 'Valhein', 'Dol', 'Earl', 'Cedria', 'Azulei', 'Yun', 'Cybel',
    'Ina', 'Foolly', 'Skili', 'Juddol', 'Janver', 'Viska', 'Hirschendy', 'Silka', 'Hellsturn', 'Essa',
    'Mykonos', 'Fenton', 'Tyrena', 'Inqoul', 'Mankov', 'Derilia', 'Hexema', 'Wyton', 'Kaedum', 'Gouram',
    'Libertia', 'Berasailles', 'Juxta', 'Tae’hr', 'Comtol', 'Gherak', 'Hest', 'Qony', 'Masamka', 'Twyll',
    'Tenos', 'Axim', 'Westrynda', 'Saphros', 'Olkham', 'Handok', 'Kemetra', 'Yos', 'Wentingle', 'Ames',
    'Molosh', 'Inkov', 'Phasasia', 'Ziedinghal', 'Bregul', 'Eishvack', 'Lora', 'Krenting', 'Symbole',
    'Elignoir', 'Keligkrul', 'Qwey', 'Vindinglag', 'Kusakira', 'Weme', 'Fayd', 'Rushvita', 'Vulkor',
    'Amers', 'Ortos', 'Vanius', 'Chandellia', 'Lilikol', 'Catca', 'Cormus', 'Yuela', 'Ariban', 'Tryton',
    'Fesscha', 'Opalul', 'Zakzos', 'Hortimer', 'Anklos', 'Dushasiez', 'Polop', 'Mektal', 'Orinphus',
    'Denatra', 'Elkazzi', 'Dyne', 'Domos', 'Letryal', 'Manniv', 'Sylestia', 'Esnol', 'Fasafuros',
    'Ghanfer', 'Kahnite', 'Sweyda', 'Uylis', 'Retenia', 'Bassos', 'Arkensval', 'Impelos', 'Grandius',
    'Fulcrux', 'Lassahein', 'Edsveda', 'Earakun', 'Fous', 'Maas', 'Basenphal', 'Jubidya', 'Divya',
    'Kosunten', 'Ordayius', 'Dozzer', 'Gangher', 'Escha', 'Manchul', 'Kempos', 'Kulo', 'Urtench',
    'Kesta', 'Helahona', 'Ryte', 'Falcia', 'Umannos', 'Urkensvall', 'Fedra', 'Bulkensar', 'Comia',
    'Tyul', 'Lasendarl'
]


class Race:
    """Basic characteristics for race"""
    race = 'Unknown'
    speed = 30
    strength_bonus = 0
    dexterity_bonus = 0
    constitution_bonus = 0
    intelligence_bonus = 0
    wisdom_bonus = 0
    charisma_bonus = 0
    hp_bonus = 0


class Dwarf(Race):
    """"""
    race = 'Dwarf'
    constitution_bonus = 2


class Dragonborn(Race):
    """"""
    race = 'Dragonborn'
    strength_bonus = 2
    charisma_bonus = 1


class Elf(Race):
    """"""
    race = 'Elf'
    dexterity_bonus = 2


class Gnome(Race):
    """"""
    race = 'Gnome'
    intelligence_bonus = 2


class HalfElf(Race):
    """"""
    race = 'Half-Elf'
    charisma_bonus = 2
    intelligence_bonus = 1
    wisdom_bonus = 1


class Halfling(Race):
    """"""
    race = 'Halfling'
    dexterity_bonus = 2


class HalfOrc(Race):
    """"""
    race = 'Half-Orc'
    strength_bonus = 2
    constitution_bonus = 1


class Human(Race):
    """"""
    race = 'Human'
    strength_bonus = 1
    constitution_bonus = 1
    intelligence_bonus = 1
    dexterity_bonus = 1
    wisdom_bonus = 1
    charisma_bonus = 1


class Tiefling(Race):
    """"""
    race = 'Tiefling'
    charisma_bonus = 2
    intelligence_bonus = 1


race_list = [
    Dwarf,
    Dragonborn,
    Elf,
    Gnome,
    HalfElf,
    Halfling,
    HalfOrc,
    Human,
    Tiefling
]
