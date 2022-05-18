#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Players:
    """Methods for handling all players"""
    def __init__(self, player_list):
        """
        :param player_list: list of dict, players in channel
        """
        self.player_list = self.load_players_in_channel(player_list)

    def load_players_in_channel(self, player_list, refresh=False):
        """Loads all the human players in the channel"""
        if refresh:
            # Check if someone hasn't yet been added, but preserve other players
            for p in player_list:
                if self.get_player_index_by_id(p['id']) is None:
                    # Player not in list
                    self.player_list.append(Player(p['id'], p['display_name']))
                else:
                    player = self.get_player_by_id(p['id'])
                    # Ensure the display_name is up to date
                    player.display_name = p['display_name']
        else:
            plist = []
            for p in player_list:
                plist.append(Player(p['id'], p['display_name']))
            return plist

    def get_player_ids(self):
        """Collect user ids from a list of players"""
        return [x.player_id for x in self.player_list]

    def get_player_index_by_id(self, player_id):
        """Returns the index of a player in a list of players that has a matching 'id' value"""
        matches = [x for x in self.player_list if x.player_id == player_id]
        if len(matches) > 0:
            return self.player_list.index(matches[0])
        return None

    def get_player_by_id(self, player_id):
        """Returns a dictionary of player info that has a matching 'id' value in a list of player dicts"""
        player_idx = self.get_player_index_by_id(player_id)
        if player_idx is not None:
            return self.player_list[player_idx]
        return None

    def update_player(self, player_id, player_obj):
        """Updates the player's object by finding its position in the player list"""
        player_idx = self.get_player_index_by_id(player_id)
        self.player_list[player_idx] = player_obj


class Player:
    """Player-specific things"""

    def __init__(self, player_id, display_name):
        self.player_id = player_id
        self.player_tag = '<@{}>'.format(self.player_id)
        self.display_name = display_name
        self.character_list = list()

    def get_char_by_name(self, name):
        """Returns character obj by lowercase name"""
        if name in [x.name_lower for x in self.character_list]:
            return [x for x in self.character_list if x.name_lower == name][0]
        return None

    def remove_char_by_name(self, name):
        """Removes character obj by lowercase name"""
        char = self.get_char_by_name(name)
        if char is not None:
            _ = self.character_list.pop(self.character_list.index(char))
            return True
        return False
