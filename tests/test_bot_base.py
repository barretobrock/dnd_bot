import re
from unittest import TestCase, main
from unittest.mock import MagicMock
from pukr import get_logger
from dnd.bot_base import DNDBot
from tests.common import make_patcher
from tests.mocks.users import random_user


class TestDNDBot(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.log = get_logger('test_dnd')
        cls.dndbot = None

    def setUp(self) -> None:
        self.mock_eng = MagicMock(name='PSQLClient')
        self.mock_session = self.mock_eng.session_mgr.return_value.__enter__.return_value
        # Load how to return things from the various ORM paths
        self.mock_session.query.return_value.join.return_value.filter.return_value.group_by.return_value\
            .all.side_effect = self._side_effect_query_stmt_decider
        self.mock_creds = make_patcher(self, 'dnd.bot_base.SimpleNamespace')
        self.mock_slack_base = make_patcher(self, 'dnd.bot_base.SlackBotBase')
        self.mock_game = MagicMock(name='Game')
        if self.dndbot is None:
            self.dndbot = DNDBot(eng=self.mock_eng, bot_cred_entry=self.mock_creds, parent_log=self.log)

    def test_init(self):
        # Assert greater than 10 entries
        self.assertGreater(len(self.dndbot.commands), 2)
        self.mock_eng.get_setting.assert_called()
        self.mock_slack_base.assert_called()

    def _side_effect_query_stmt_decider(self, *args, **kwargs):
        """Decides which mocked pandas query to IMLdb to return based on the select arguments provided"""
        # Check the most recent call; if the arguments in query match what's below, return the designated result
        select_cols = [x.__dict__.get('key') for x in self.mock_session.query.call_args.args]
        if select_cols == ['player_id', 'display_name', 'overall']:
            # This is mainly illustrative until the db is loaded. No queries are running on the db at this moment.
            pass
        else:
            raise ValueError(f'Unaccounted query condition for these selections: {select_cols}')

    def test_roll_determine(self):
        """Tests the roll_determine method"""
        cases = {
            'roll 1d20': re.compile(r'1d20 \(~*\**\d+\**~*\) = `~*\**\d+~*\**`'),
            'roll (1d4 + 1, 3, 2d6kl1)kh1': re.compile(r'\(~*1d4 \(~*\**\d~*\**\) \+ \d~*, ~*\d~*, ~*2d6kl1 '
                                                       r'\(~*\**\d\**~*, ~*\**\d\**~*\)~*\)kh1 = `~*\**\d+~*\**`'),
            'roll 2d20 - 2 + 4d10': re.compile(r'2d20 \([*~\d,\s]+\) - 2 \+ 4d10 '
                                               r'\([*~\d,\s]+\) = `\d+`'),
            'r d8': re.compile(r'1d8 \(~*\**\d+~*\**\) = `~*\**\d+~*\**`'),
            'roll 8d6mi2': re.compile(r'8d6mi2 \([*~\d,->\s]+\) = `~*\**\d+~*\**`'),
            'r d15': re.compile(r'1d15 \(~*\**\d+~*\**\) = `~*\**\d+~*\**`'),
            'r 3d6 [fire] + 1d4 [piercing]': re.compile(r'3d6 \([*~\d,\s]+\) \[fire] \+ 1d4 \([*~\d,\s]+\) '
                                                        r'\[piercing] = `~*\**\d+~*\**`'),
            'r direction': re.compile(r'`\w+`'),
            'roll stats': re.compile(r'[A-Z]{3}: \d+ \([-+]\d+\)\n?' * 6)
        }
        for msg, outcome in cases.items():
            resp = self.dndbot.roll_determine(message=msg)
            if isinstance(outcome, re.Pattern):
                # Confirm pattern matches
                self.assertRegex(resp, expected_regex=outcome)

    def test_character_generator(self):
        """Tests the character_generator method"""
        resp = self.dndbot.character_generator(user=random_user(), message='chargen')


if __name__ == '__main__':
    main()
