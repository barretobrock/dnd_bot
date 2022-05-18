"""Configuration setup"""
from dnd import (
    __version__,
    __update_date__
)


class Common(object):
    """Configuration items common across all config types"""
    BOT_FIRST_NAME = 'Dizzy Boborkadork'
    BOT_NICKNAME = 'dizzy'
    ADMINS = ['UM35HE6R5']
    TRIGGERS = ['dizzy', 'd!']

    VERSION = __version__
    UPDATE_DATE = __update_date__


class Development(Common):
    """Configuration for development environment"""
    ENV = 'DEV'
    BOT_LAST_NAME = 'Debugdindov'
    MAIN_CHANNEL = 'C02MKMBF1NW'
    TRIGGERS = ['fizzy', 'f!']
    DEBUG = True


class Production(Common):
    """Configuration for development environment"""
    ENV = 'PROD'
    BOT_LAST_NAME = 'Prodnodindov'
    MAIN_CHANNEL = 'CPDN3QLMU'
    TRIGGERS = ['dizzy', 'd!']
    DEBUG = False
