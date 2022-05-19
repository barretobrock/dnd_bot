#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
from datetime import datetime
from typing import (
    Dict,
    List,
    Optional
)
from types import SimpleNamespace
from loguru import logger
from slacktools import (
    SlackBotBase,
    BlockKitBuilder as BKitB
)
from slacktools.tools import build_commands
from dnd import ROOT_PATH
from dnd.db_eng import DizzyPSQLClient
from dnd.model import (
    SettingType
)
from dnd.settings import auto_config
from dnd.core.dice import (
    roll_dice,
    dir_roll,
    stats_roll
)
from dnd.core.characters import random_char_gen


class DNDBot:
    """Bot for practicing DnD combat on Slack"""

    def __init__(self, eng: DizzyPSQLClient, bot_cred_entry: SimpleNamespace, parent_log: logger):
        """
        Args:

        """
        self.bot_name = f'{auto_config.BOT_FIRST_NAME} {auto_config.BOT_LAST_NAME}'
        self.log = parent_log.bind(child_name=self.__class__.__name__)
        self.eng = eng
        self.triggers = auto_config.TRIGGERS
        self.channel_id = auto_config.MAIN_CHANNEL  # cah or cah-test
        self.admin_user = auto_config.ADMINS
        self.version = auto_config.VERSION
        self.update_date = auto_config.UPDATE_DATE

        # Begin loading and organizing commands
        self.commands = build_commands(self, cmd_yaml_path=ROOT_PATH.parent.joinpath('commands.yaml'),
                                       log=self.log)
        # Initate the bot, which comes with common tools for interacting with Slack's API
        self.st = SlackBotBase(bot_cred_entry=bot_cred_entry, triggers=self.triggers, main_channel=self.channel_id,
                               parent_log=self.log, debug=False, use_session=False)
        # Pass in commands to SlackBotBase, where task delegation occurs
        self.log.debug('Patching in commands to SBB...')
        self.st.update_commands(commands=self.commands)
        self.bot_id = self.st.bot_id
        self.user_id = self.st.user_id
        self.bot = self.st.bot
        self.generate_intro()

        if self.eng.get_setting(SettingType.IS_ANNOUNCE_STARTUP):
            self.log.debug('IS_ANNOUNCE_STARTUP was enabled, so sending message to main channel')
            self.st.message_main_channel(blocks=self.get_bootup_msg())

    def get_bootup_msg(self) -> List[Dict]:
        return [BKitB.make_context_section([
            BKitB.markdown_section(f"*{self.bot_name}* *`{self.version}`* booted up at `{datetime.now():%F %T}`!"),
            BKitB.markdown_section(f"(updated {self.update_date})")
        ])]

    def search_help_block(self, message: str):
        """Takes in a message and filters command descriptions for output
        """
        self.log.debug(f'Got help search command: {message}')
        return self.st.search_help_block(message=message)

    def generate_intro(self):
        """Generates the intro message and feeds it in to the 'help' command"""
        intro = f"Hi! I'm *{self.bot_name}* and I am help you to Dungeon and Dragon! \n" \
                f"Be sure to call my attention first with *`{'`* or *`'.join(self.triggers)}`*\n " \
                f"Example: *`d! roll d20`*\nHere's what I can do:"
        avi_url = "https://avatars.slack-edge.com/2019-10-13/782232259363_98821cb8199a6c08a095_512.jpg"
        avi_alt = 'dat me'
        # Build the help text based on the commands above and insert back into the commands dict
        return self.st.build_help_block(intro, avi_url, avi_alt)

    def cleanup(self, *args):
        """Runs just before instance is destroyed"""
        _ = args
        notify_block = [
            BKitB.make_context_section([BKitB.markdown_section(f'{self.bot_name} died. '
                                                               f':death-drops::party-dead::death-drops:')])
        ]
        if self.eng.get_setting(SettingType.IS_ANNOUNCE_SHUTDOWN):
            self.st.message_main_channel(blocks=notify_block)
        self.log.info('Bot shutting down...')
        sys.exit(0)

    def process_slash_command(self, event_dict: Dict):
        """Hands off the slash command processing while also refreshing the session"""
        # TODO: Log slash
        self.st.parse_slash_command(event_dict)

    def process_event(self, event_dict: Dict):
        """Hands off the event data while also refreshing the session"""
        self.st.parse_event(event_data=event_dict)

    def process_incoming_action(self, user: str, channel: str, action_dict: Dict, event_dict: Dict,
                                ) -> Optional:
        """Handles an incoming action (e.g., when a button is clicked)"""
        action_id = action_dict.get('action_id')
        action_value = action_dict.get('value')
        msg = event_dict.get('message', {})
        _ = msg.get('thread_ts')
        self.log.debug(f'Receiving action_id: {action_id} and value: {action_value} from user: {user} in '
                       f'channel: {channel}')
        if action_id == 'new-char-create':
            pass
        else:
            pass

    def character_generator(self, user: str, message: str) -> str:
        """Handles character generation"""
        self.log.debug('Spinning up random character.')
        msg_split = message.split()
        name = None
        if '-n' in msg_split:
            # Apply a name provided by the user
            name = ' '.join(msg_split[msg_split.index('-n') + 1:])
        char = random_char_gen(user, name)
        return char.info_blocks()

    def roll_determine(self, message: str) -> str:
        """Determine which roll function to use"""
        cmd = re.sub(r'^(roll|r)\s+', '', message).strip()
        self.log.debug(f'Stripped roll command to: {cmd}')
        if 'stats' in message:
            return '\n'.join([x['ability'].__repr__() for x in stats_roll()])
        elif 'direction' in message:
            return f'`{dir_roll()}`'
        elif re.match(r'[\(\)d\d\s+-\/*]+', cmd, re.IGNORECASE) is not None:
            try:
                return roll_dice(cmd, str_output=True)
            except SyntaxError:
                return f'I wasn\'t able to parse out this roll command: {message}. ' \
                       f'Here\'s an example of what I do understand: `r 1d20 + 6 + 4d6`'
        else:
            return f'I didn\'t understand the syntax after \'roll\' for this: `{cmd}`'
