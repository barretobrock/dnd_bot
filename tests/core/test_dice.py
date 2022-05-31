import re
from unittest import (
    TestCase,
    main
)
from pukr import get_logger
from dnd.core.dice import (
    MaxRollsExceededException,
    MaxSidesExceededException,
    roll_dice
)


class TestDice(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.log = get_logger('dice_test')

    def test_roll(self):
        cases = {
            'd20': re.compile(r'1d20 \(~*\**\d+\**~*\) = `~*\**\d+~*\**`'),
            '1000d10000000000000': MaxSidesExceededException(),
            '1000d100': MaxRollsExceededException(),
            '1d51 * 40d50 + 58d100': MaxSidesExceededException(),
            '1d20 + 40d50 + 30d100 + 4d30': re.compile(r'1d20 \([*~\d,\s]+\) \+ 40d50 \([*~\d,\s]+\) \+ 30d100 '
                                                       r'\([*~\d,\s]+\) \+ 4d30 \([*~\d,\s]+\) = `~*\**\d+~*\**`'),
            'd15': re.compile(r'1d15 \(~*\**\d+~*\**\) = `~*\**\d+~*\**`'),
            '3d6 [fire] + 1d4 [piercing]': re.compile(r'3d6 \([*~\d,\s]+\) \[fire] \+ 1d4 \([*~\d,\s]+\) '
                                                      r'\[piercing] = `~*\**\d+~*\**`'),
            '(1d4 + 1, 3, 2d6kl1)kh1': re.compile(r'\(~*1d4 \(~*\**\d~*\**\) \+ \d~*, ~*\d~*, ~*2d6kl1 '
                                                  r'\(~*\**\d\**~*, ~*\**\d\**~*\)~*\)kh1 = `~*\**\d+~*\**`'),
            '2d20 - 2 + 4d10': re.compile(r'2d20 \([*~\d,\s]+\) - 2 \+ 4d10 '
                                          r'\([*~\d,\s]+\) = `\d+`'),
        }
        for cmd, outcome in cases.items():
            self.log.debug(f'Running with command: {cmd}')
            if isinstance(outcome, (MaxSidesExceededException, MaxRollsExceededException)):
                with self.assertRaises(type(outcome)) as err:
                    _ = roll_dice(input_txt=cmd, str_output=True)
                self.assertIn('User exceeded the maximum', str(err.exception))
                continue
            resp = roll_dice(input_txt=cmd, str_output=True)
            if isinstance(outcome, re.Pattern):
                # Confirm pattern matches
                self.assertRegex(resp, expected_regex=outcome)


if __name__ == '__main__':
    main()
