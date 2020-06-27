"""Util tests"""
import os
import unittest
from dnd.bot import DNDBot


bot_name = 'dnd'
key_path = os.path.join(os.path.expanduser('~'), 'keys')
key_dict = {}
for t in ['SIGNING_SECRET', 'XOXB_TOKEN', 'XOXP_TOKEN', 'VERIFY_TOKEN']:
    with open(os.path.join(key_path, f'{bot_name.upper()}_SLACK_{t}')) as f:
        key_dict[t.lower()] = f.read().strip()


class TestViktor(unittest.TestCase):
    dnd = DNDBot(bot_name, key_dict['xoxb_token'], key_dict['xoxp_token'])
    user_me = 'UM35HE6R5'  # me
    test_channel = 'CM376Q90F'   # test
    trigger = dnd.triggers[0]
