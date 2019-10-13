#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dnd import DNDBot
from kavalkilu import Log, LogArgParser


# Initiate logging
log = Log('dnd', log_lvl=LogArgParser().loglvl)

dndbot = DNDBot(log)
try:
    dndbot.run_rtm('Booted up and ready to play! :hyper-tada:', 'Daemon killed gracefully. :party-dead:')
except KeyboardInterrupt:
    log.debug('Script ended manually.')
finally:
    dndbot.message_grp('Shutdown for maintenance.:dotdotdot:')

log.close()

