#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import time
import signal
import traceback
from random import shuffle
from slacktools import SlackTools
from kavalkilu import Keys
from .dice import dice_roller, dir_roll, stats_roll


help_txt = """
*Command Prefix*
 - `d!` or `dnd`: Use this before any of the below commands (e.g., `d! roll d20`)

*Basic Commands (currently inactive)*:
 - `combat [OPTIONS]`: Begin a new combat round 
    flags:
        - `-cr [1-5]`: Set the challenge rating (this determines enemy stats, numbers) 
        - `-p character1 character2`: Set the players taking part in the combat 
 - `stats <character_name>`: Get stats on the character

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


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


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

        # For storing game info
        self.game_dict = {
            'players': self.build_players(),
            'ping-judge': False,
            'status': 'stahted'
        }
        self.cah_gsheet = k.get_key('cah_sheet')
        self.set_dict = self.st.read_in_sheets(self.cah_gsheet)

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

    def handle_command(self, channel, message, user):
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
        elif message != '':
            response = "I didn't understand this: `{}`\n " \
                       "Use `cah help` to get a list of my commands.".format(message)

        if response is not None:
            resp_dict = {
                'user': user
            }
            self.st.send_message(channel, response.format(**resp_dict))

    def message_grp(self, message):
        """Wrapper to send message to whole channel"""
        self.st.send_message(self.channel_id, message)

    def _determine_card_set(self, message_split):
        """Determines which card set to use"""
        if any([x in message_split for x in ['-set', '-s']]) and len(message_split) > 3:
            # We're going to skip some players
            set_idx = None
            for s in ['-set', '-s']:
                try:
                    set_idx = message_split.index(s)
                    break
                except ValueError:
                    continue
            card_set = message_split[set_idx + 1].strip()
            notify_msg = 'Using `{}` card set'.format(card_set)
        else:
            card_set = 'standard'
            notify_msg = 'Using `{}` card set'.format(card_set)

        return notify_msg, card_set

    def _determine_players(self, message_split):
        """Determines the players for the game"""

        # Our regular set of players, defined as any non-bot channel members
        players = self.game_dict['players']

        if '-p' in message_split and len(message_split) > 3:
            # We're going to play with only some players of the channel
            play_idx = message_split.index('-p')
            specific_player_ids = [x for x in message_split[play_idx + 1:] if '<@' in x]
        else:
            specific_player_ids = None

        if specific_player_ids is not None:
            # This game is set with specific players
            player_ids = []
            for p in specific_player_ids:
                # Extract user id
                uid = self.st.parse_tag_from_text(p)
                if uid is None:
                    # Failed at parsing
                    self.message_grp('Failed to parse a user id for `{}`. Game cannot proceed.'.format(p))
                    return None
                else:
                    player_ids.append(uid)

            for player in players:
                # Skip player if not in our list of ids
                player['skip'] = player['id'] not in player_ids

            # Build the notification message
            notify_msg = 'Skipping: `{}`'.format('`,`'.join([x['display_name'] for x in players if x['skip']]))
        else:
            notify_msg = 'Playing with everyone.'

        # Reload new player data
        self.game_dict['players'] = players
        return notify_msg

    def new_game(self, message):
        """Begins a new game"""
        msg_split = message.split()
        response_list = []

        # Determine card set to use
        card_set_msg, card_set = self._determine_card_set(msg_split)
        response_list.append(card_set_msg)
        cards = self._read_in_cards(set_type=card_set)
        if cards is not None:
            black_cards = cards['q']
            white_cards = cards['a']
            # Shuffle cards
            shuffle(black_cards)
            shuffle(white_cards)
        else:
            return None

        response_list.append('Cards have been shuffled. Generating players...')
        # Refresh the players' names
        self.refresh_players()
        player_notification = self._determine_players(msg_split)
        if player_notification is None:
            return None
        else:
            response_list.append(player_notification)
        players = self.game_dict['players']

        shuffle(players)
        response_list.append('Judge order: {}'.format(' :finger-wag-right: '.join(
            [x['display_name'] for x in players if not x['skip']])))

        # store game details in a dict
        self.game_dict.update({
            'status': 'initiated',
            'players': players,
            'player_names': ','.join([x['display_name'] for x in players]),
            'judge': [x for x in players if not x['skip']][0],
            'remaining_white': white_cards,
            'remaining_black': black_cards,
        })

        # Kick off the new round, message details to the group
        self.new_round(notifications=response_list, replace_all=True)

    def build_players(self):
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
                'skip': False,
                'dm_cards': False,
                'score': 0
            }
            # Make sure display name is not empty
            if user_cleaned['display_name'] == '':
                user_cleaned['display_name'] = user_cleaned['real_name']
            players.append(user_cleaned)
        return players

    def get_player_ids(self, player_list):
        """Collect user ids from a list of players"""
        return [x['id'] for x in player_list]

    def get_player_index_by_id(self, player_id, player_list):
        """Returns the index of a player in a list of players that has a matching 'id' value"""
        return player_list.index([x for x in player_list if x['id'] == player_id][0])

    def get_player_by_id(self, player_id, player_list):
        """Returns a dictionary of player info that has a matching 'id' value in a list of player dicts"""
        player_idx = self.get_player_index_by_id(player_id, player_list)
        return player_list[player_idx]

    def refresh_players(self):
        """Refreshed existing player names and adds new players that may have joined the channel"""
        players = self.game_dict['players']
        refreshed_players = self.build_players()
        for refreshed_player in refreshed_players:
            refreshed_player_id = refreshed_player['id']
            if refreshed_player_id in self.get_player_ids(players):
                # Existing player, avoid updating score, prefs, but refresh names
                player_idx = self.get_player_index_by_id(refreshed_player_id, players)
                for key in ['display_name', 'real_name']:
                    if refreshed_player[key] != players[player_idx][key]:
                        players[player_idx][key] = refreshed_player[key]
                # Update player in list
                players[player_idx] = refreshed_player
            else:
                # New player
                players.append(refreshed_player)
        self.game_dict['players'] = players

    # Player-triggered functions
    def show_help(self):
        """Prints help statement to channel"""
        self.message_grp(help_txt)

    def roll_determine(self, msg):
        """Determine which roll function to use"""

        if re.match(r'\d*d\d+', msg, re.IGNORECASE):
            try:
                res = dice_roller(msg.replace('roll', '').strip())
                self.message_grp(res)
            except SyntaxError:
                self.message_grp("I wasn't able to parse out the roll command. Example syntax: `1d20 + 6 + 4d6`")
        elif 'stats' in msg:
            self.message_grp(stats_roll())
        elif 'direction' in msg:
            self.message_grp(dir_roll())

