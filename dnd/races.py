#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Race:
    """Basic characteristics for race"""

    def __init__(self, **attrs):
        self.race = 'Unknown'
        self.speed = 30
        self.strength_bonus = 0
        self.dexterity_bonus = 0
        self.constitution_bonus = 0
        self.intelligence_bonus = 0
        self.wisdom_bonus = 0
        self.charisma_bonus = 0
        self.hp_bonus = 0
        self.name_list = [
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

        for k, v in attrs.items():
            # Set any other attributes added in
            self.__setattr__(k, v)


class Dwarf(Race):
    """"""

    def __init__(self, **attrs):
        attrs.update({
            'race': 'Dwarf',
            'constitution_bonus': 2,
        })
        super().__init__(**attrs)


class Dragonborn(Race):
    """"""

    def __init__(self, **attrs):
        attrs.update({
            'race': 'Dragonborn',
            'strength_bonus': 2,
            'charisma_bonus': 1,
        })
        super().__init__(**attrs)


class Elf(Race):
    """"""

    def __init__(self, **attrs):
        attrs.update({
            'race': 'Elf',
            'dexterity_bonus': 2,
        })
        super().__init__(**attrs)


class Gnome(Race):
    """"""

    def __init__(self, **attrs):
        attrs.update({
            'race': 'Gnome',
            'intelligence_bonus': 2,
        })
        super().__init__(**attrs)


class HalfElf(Race):
    """"""

    def __init__(self, **attrs):
        attrs.update({
            'race': 'Half-Elf',
            'charisma_bonus': 2,
            'intelligence_bonus': 1,
            'wisdom_bonus': 1,
        })
        super().__init__(**attrs)


class Halfling(Race):
    """"""

    def __init__(self, **attrs):
        attrs.update({
            'race': 'Halfling',
            'dexterity_bonus': 2,
        })
        super().__init__(**attrs)


class HalfOrc(Race):
    """"""

    def __init__(self, **attrs):
        attrs.update({
            'race': 'Half-Orc',
            'strength_bonus': 2,
            'constitution_bonus': 1,
        })
        super().__init__(**attrs)


class Human(Race):
    """"""

    def __init__(self, **attrs):
        attrs.update({
            'race': 'Human',
            'strength_bonus': 1,
            'constitution_bonus': 1,
            'intelligence_bonus': 1,
            'dexterity_bonus': 1,
            'wisdom_bonus': 1,
            'charisma_bonus': 1,
        })
        super().__init__(**attrs)


class Tiefling(Race):
    """"""

    def __init__(self, **attrs):
        attrs.update({
            'race': 'Tiefling',
            'charisma_bonus': 2,
            'intelligence_bonus': 1,
        })
        super().__init__(**attrs)


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
