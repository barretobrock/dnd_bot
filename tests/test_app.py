from unittest import TestCase, main
from unittest.mock import (
    patch,
    MagicMock
)
from pukr import get_logger
from tests.common import random_string


class TestApp(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.log = get_logger('dnd_test')


if __name__ == '__main__':
    main()
