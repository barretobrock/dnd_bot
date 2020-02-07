#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from slacktools import SlackTools, GSheetReader
from .dice import roll_dice, dir_roll, stats_roll
from .characters import random_char_gen
from .players import Players


help_txt = """
*Command Prefix*
 - `f!` or `felix`: Use this before any of the below commands (e.g., `f! roll d20`)

*Basic Commands*:
 - `gen char [OPTIONS]`: generate a new character with random stats. 
    flags:
        - `-n <name>`:  give the character a specific name (otherwise randomly assigned)
        - `-race <race>`: assign a race to the character
        - `-class <class>`: assign a class to the character
        - `-stats <stats>`: assign the character comma-separated stats 
 - `my chars`: list the names of all your characters
 - `stats <name>`: get stats on the character
 - `rm char <name>`: remove a character by name from your catalog

*Dice Rolling*:
 - `roll <rolls>d<sides>`: roll (and add) dice using standard notation
    Examples:
        `roll 1d20 + 8 + 4d8`
        `roll 2d20 - 2 + 4d10`
        `roll d20`
        `roll 2 + 2 + 5d8`
 - `roll stats`: returns the results for a DnD 5e stats roll (4d6 drop lowest)
 - `roll direction`: determines direction to travel based on roll

:point-down: *NOT YET READY* :point-down:
*Combat Initiation*:
 - `combat [OPTIONS]`: Begin a new combat session 
    option flags:
        - `-cr [1-5]`: Set the challenge rating (this determines enemy stats, numbers) 
        - `-t1 character1 character2`: Set the characters in team 1
        - `-t2 character1 character2`: Set the characters in team 2 

*In-Combat Commands (currently inactive)*
 - `attack [OPTIONS]`
    flags:
        - `-w [slot-number]`: Attack with weapon in slot <n>. Otherwise will use primary
 - `continue`: proceeds to the next round of combat 
 - `to the end`: fast-forwards combat until a team surrenders
 - `surrender`: ends the combat round before a resolution is made automatically
"""


class DNDBot:
    """Bot for practicing DnD combat on Slack"""

    def __init__(self, log_name, xoxb_token, xoxp_token, debug=False):
        """
        :param log_name: str, name of the log to retrieve
        :param debug: bool,
        """
        self.bot_name = 'Felix'
        self.triggers = ['felix', 'f!'] if not debug else ['ftest', 'ft!']
        self.channel_id = 'CSQKP7S90' if not debug else 'CT48WCESG'  # random or felix-test
        # Read in common tools for interacting with Slack's API
        self.st = SlackTools(log_name, triggers=self.triggers, team='dd-indeed',
                             xoxp_token=xoxp_token, xoxb_token=xoxb_token)
        # Two types of API interaction: bot-level, user-level
        self.bot = self.st.bot
        self.user = self.st.user
        self.bot_id = self.bot.auth_test()['user_id']

        # For storing game info
        self.dnd_gsheet = '19BQ9yevHj68YaEhHaD5-7Eu32BQSpXXJDdYo4CNkaOA'
        self.gs_dict = {}
        self._read_in_sheets()

        self.players = Players(self._build_players())

    def handle_command(self, event_dict):
        """Handles a bot command if it's known"""
        # Simple commands that we can map to a function
        commands = {
            'help': self.show_help,
            'good bot': 'thanks <@{user}>!',
            'gsheets link': self.show_gsheet_link(),
            # 'status': self.display_status,
            # 'surrender': self.end_game,

        }
        response = None
        message = event_dict['message']
        raw_message = event_dict['raw_message']
        user = event_dict['user']
        channel = event_dict['channel']

        if message in commands.keys():
            # Call the command
            commands[message]()
            return None
        if message.startswith('roll'):
            self.roll_determine(message, channel)
        elif message.startswith('gen char'):
            response = self.character_generator(user, raw_message)
        elif message == 'my chars':
            response = self.show_user_chars(user)
        elif message == 'refresh sheets':
            self._read_in_sheets()
            response = 'Sheets have been refreshed! `{}`'.format(','.join(self.gs_dict.keys()))
        elif message.startswith('stats'):
            response = self.get_char_stats(user, message)
        elif message.startswith('rm char'):
            response = self.remove_character(user, message)
        elif message != '':
            response = "I didn't understand this: `{}`\n " \
                       "Use `felix help` to get a list of my commands.".format(message)

        if response is not None:
            resp_dict = {
                'user': user
            }
            self.st.send_message(channel, response.format(**resp_dict))

    def message_grp(self, message, channel=None):
        """Wrapper to send message to whole channel"""
        channel = self.channel_id if channel is None else channel
        self.st.send_message(channel, message)

    def character_generator(self, user, message):
        """Handles character generation"""
        msg_split = message.split()
        name = None
        if '-n' in msg_split:
            # Apply a name provided by the user
            name = ' '.join(msg_split[msg_split.index('-n') + 1:])
        player = self.players.get_player_by_id(user)
        char = random_char_gen(user, name)
        player.character_list.append(char)
        self.players.update_player(user, player)
        return char.__repr__()

    def show_user_chars(self, user):
        """Shows the name of the users characters"""
        player = self.players.get_player_by_id(user)
        c_list = player.character_list
        char_info = []
        if len(c_list) > 0:
            for char in c_list:
                char_str = '`{}` ({} {})'.format(char.name, char.race, char.char_class)
                char_info.append(char_str)
            return '\n'.join(char_info)
        return 'No characters to show!'

    def get_char_stats(self, user, message):
        """Shows the stats of a particular character"""
        player = self.players.get_player_by_id(user)
        char = player.get_char_by_name(message.replace('stats', '').strip())
        return char.__repr__()

    def remove_character(self, user, message):
        player = self.players.get_player_by_id(user)
        char_name = message.replace('rm char', '').strip()
        success = player.remove_char_by_name(char_name)
        if success:
            return 'Character `{}` successfully removed.'.format(char_name)
        else:
            return 'Could not remove `{}`.'.format(char_name)

    def _build_players(self):
        """
        Takes in a list of users in channel, sets basic, game-related details and
            returns a list of dicts for each human player
        """
        players = []
        for user in self.st.get_channel_members(self.channel_id, humans_only=True):
            user_cleaned = {
                'id': user['id'],
                'display_name': user['display_name'].lower(),
                'real_name': user['name'],
                'is_bot': user['is_bot'],
            }
            # Make sure display name is not empty
            if user_cleaned['display_name'] == '':
                user_cleaned['display_name'] = user_cleaned['real_name']
            players.append(user_cleaned)
        return players

    def _refresh_players(self):
        """Refreshed existing player names and adds new players that may have joined the channel"""
        self.players.load_players_in_channel(self._build_players(), refresh=True)

    # Player-triggered functions
    def show_help(self, channel=None):
        """Prints help statement to channel"""
        self.message_grp(help_txt, channel)

    def _read_in_sheets(self):
        """Reads in GSheets for Viktor"""
        gs = GSheetReader(self.dnd_gsheet)
        sheets = gs.sheets
        self.gs_dict = {}
        for sheet in sheets:
            self.gs_dict.update({
                sheet.title: gs.get_sheet(sheet.title)
            })

    def roll_determine(self, msg, channel=None):
        """Determine which roll function to use"""
        cmd = msg.replace('roll', '').strip()
        if re.match(r'((\d+|\+| +)|(\d*)d(\d+))', cmd, re.IGNORECASE) is not None:
            try:
                res = roll_dice(cmd, str_output=True)
                self.message_grp(res, channel)
            except SyntaxError:
                self.message_grp("I wasn't able to parse out the roll command. Example syntax: `1d20 + 6 + 4d6`",
                                 channel)
        elif 'stats' in msg:
            self.message_grp('\n'.join([x['ability'].__repr__() for x in stats_roll()]), channel)
        elif 'direction' in msg:
            self.message_grp('`{}`'.format(dir_roll()), channel)
        else:
            self.message_grp("I didn't understand the syntax after 'roll' for this: `{}`".format(cmd), channel)

    def show_gsheet_link(self):
        """Prints a link to the gsheet in the channel"""

        return f'https://docs.google.com/spreadsheets/d/{self.dnd_gsheet}/'

