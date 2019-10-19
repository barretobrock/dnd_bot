#!/usr/bin/env python3
# -*- coding: utf-8 -*-




class Game:
    """Game elements"""

    def __init__(self, players):
        self.players = players



class Status:
    """Game status"""
    statuses = [
        'initiated',
        'game_started',
        'combat',
        'game_ended'
    ]

    def __init__(self):
        self.status = self.statuses[0]


