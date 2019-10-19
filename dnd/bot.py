#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import time
import traceback
from random import shuffle
from slacktools import SlackTools, GracefulKiller
from kavalkilu import Keys
from .dice import roll_dice, dir_roll, stats_roll
from .characters import random_char_gen
from .players import Players


help_txt = """
*Command Prefix*
 - `d!` or `dnd`: Use this before any of the below commands (e.g., `d! roll d20`)

*Basic Commands (currently inactive)*:
 - `gen char [OPTIONS]`: generate a new character with random stats. 
    flags:
        - `-n <name>`:  give the character a specific name (otherwise randomly assigned)
 - `combat [OPTIONS]`: Begin a new combat round 
    flags:
        - `-cr [1-5]`: Set the challenge rating (this determines enemy stats, numbers) 
        - `-p character1 character2`: Set the players taking part in the combat 
 - `my chars`: list the names of all your characters
 - `stats <name>`: get stats on the character
 - `rm char <name>`: remove a character by name from your catalog

*Dice Rolling*:
 - `roll (\\d+)d(\\d+) (+\d+|(\\d+)d(\\d+))*`: roll (and add) dice using standard notation
 - `roll stats`: returns the results for a DnD 5e stats roll (4d6 drop lowest)
 - `roll direction`: determines direction to travel based on roll

*In-Combat Commands (currently inactive)*
 - `attack [OPTIONS]`
    flags:
        - `-w [slot-number]`: Attack with weapon in slot
 - `surrender`: Ends the combat round before a resolution
"""


class DNDBot:
    """Bot for practicing DnD combat on Slack"""

    def __init__(self, log):
        self.log = log
        self.bot_name = 'Dizzy'
        self.triggers = ['dnd', 'd!']
        self.channel_id = 'CPDN3QLMU'  # #dnd
        # Read in common tools for interacting with Slack's API
        k = Keys()
        self.st = SlackTools(self.log, triggers=self.triggers, team=k.get_key('okr-name'),
                             xoxp_token=k.get_key('dizzy-token'), xoxb_token=k.get_key('dizzy-bot-user-token'))
        # Two types of API interaction: bot-level, user-level
        self.bot = self.st.bot
        self.user = self.st.user
        self.bot_id = self.bot.api_call('auth.test')['user_id']
        self.RTM_READ_DELAY = 1

        self.players = Players(self._build_players())

    def run_rtm(self, startup_msg, terminated_msg):
        """Initiate real-time messaging"""
        killer = GracefulKiller()
        if self.bot.rtm_connect(with_team_state=False):
            self.log.debug('{} is running.'.format(self.bot_name))
            self.st.send_message(self.channel_id, startup_msg)
            while not killer.kill_now:
                try:
                    msg_packet = self.st.parse_bot_commands(self.bot.rtm_read())
                    if msg_packet is not None:
                        try:
                            self.handle_command(**msg_packet)
                        except Exception as e:
                            traceback_msg = '\n'.join(traceback.format_tb(e.__traceback__))
                            exception_msg = '{}: {}'.format(e.__class__.__name__, e)
                            self.log.error(exception_msg)
                            self.st.send_message(msg_packet['channel'],
                                                 "Exception occurred: \n```{}\n{}```".format(traceback_msg,
                                                                                             exception_msg))
                    time.sleep(self.RTM_READ_DELAY)
                except Exception as e:
                    self.log.debug('Reconnecting...')
                    self.bot.rtm_connect(with_team_state=False)
            # Upon SIGTERM, message channel
            self.st.send_message(self.channel_id, terminated_msg)
        else:
            self.log.error('Connection failed.')

    def handle_command(self, channel, message, user, raw_message):
        """Handles a bot command if it's known"""
        # Simple commands that we can map to a function
        commands = {
            'help': self.show_help,
            # 'status': self.display_status,
            # 'surrender': self.end_game,

        }
        response = None
        if message in commands.keys():
            # Call the command
            commands[message]()
        if message.startswith('roll'):
            self.roll_determine(message)
        elif message.startswith('gen char'):
            response = self.character_generator(user, raw_message)
        elif message == 'my chars':
            response = self.show_user_chars(user)
        elif message.startswith('stats'):
            response = self.get_char_stats(user, message)
        elif message.startswith('rm char'):
            response = self.remove_character(user, message)
        elif message != '':
            response = "I didn't understand this: `{}`\n " \
                       "Use `dnd help` to get a list of my commands.".format(message)

        if response is not None:
            resp_dict = {
                'user': user
            }
            self.st.send_message(channel, response.format(**resp_dict))

    def message_grp(self, message):
        """Wrapper to send message to whole channel"""
        self.st.send_message(self.channel_id, message)

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
        return char

    def show_user_chars(self, user):
        """Shows the name of the users characters"""
        player = self.players.get_player_by_id(user)
        c_list = player.character_list
        return ', '.join(['`{}`'.format(x.name) for x in c_list]) if len(c_list) > 0 else 'No characters to show!'

    def get_char_stats(self, user, message):
        """Shows the stats of a particular character"""
        player = self.players.get_player_by_id(user)
        char = player.get_char_by_name(message.replace('stats', '').strip())
        return char

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
    def show_help(self):
        """Prints help statement to channel"""
        self.message_grp(help_txt)

    def roll_determine(self, msg):
        """Determine which roll function to use"""
        cmd = msg.replace('roll', '').strip()
        if re.match(r'\d*d\d+', cmd, re.IGNORECASE) is not None:
            try:
                res = roll_dice(cmd, str_output=True)
                self.message_grp(res)
            except SyntaxError:
                self.message_grp("I wasn't able to parse out the roll command. Example syntax: `1d20 + 6 + 4d6`")
        elif 'stats' in msg:
            self.message_grp(stats_roll())
        elif 'direction' in msg:
            self.message_grp(dir_roll())
        else:
            self.message_grp("I didn't understand the syntax after 'roll' for this: `{}`".format(cmd))

