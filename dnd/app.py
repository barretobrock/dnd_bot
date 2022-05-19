import signal
from flask import Flask
from slackeventsapi import SlackEventAdapter
from slacktools import SecretStore
from dnd.db_eng import DizzyPSQLClient
from dnd.settings import auto_config
from dnd.logg import get_base_logger
from dnd.bot_base import DNDBot


bot_name = auto_config.BOT_NICKNAME
logg = get_base_logger()

credstore = SecretStore('secretprops-davaiops.kdbx')
# Set up database connection
conn_dict = credstore.get_entry(f'davaidb-{auto_config.ENV.lower()}').custom_properties
dnd_creds = credstore.get_key_and_make_ns(bot_name)

logg.debug('Starting up app...')
app = Flask(__name__)
eng = DizzyPSQLClient(props=conn_dict, parent_log=logg)


logg.debug('Instantiating bot...')
Bot = DNDBot(eng=eng, bot_cred_entry=dnd_creds, parent_log=logg)

# Register the cleanup function as a signal handler
signal.signal(signal.SIGINT, Bot.cleanup)
signal.signal(signal.SIGTERM, Bot.cleanup)

# Events API listener
bot_events = SlackEventAdapter(dnd_creds.signing_secret, "/api/events", app)


@bot_events.on('message')
@logg.catch
def scan_message(event_data):
    Bot.process_event(event_data)
