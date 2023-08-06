
from telegram_bot_personnel_data_collector import arg_parse
from telegram_bot_personnel_data_collector import telegram
from telegram_bot_personnel_data_collector import google_sheets
from telegram_bot_personnel_data_collector import localisation
from telegram_bot_personnel_data_collector import session_cache
from telegram_bot_personnel_data_collector import utils
from telegram_bot_personnel_data_collector import configurations

__doc__ = """
Documents: https://core.telegram.org/bots/api
"""

version = '1.23'
author = 'Dmitry Oguz'
author_email = 'doguz2509@gmail.com'

__all__ = [
    'configurations',
    'version',
    'author',
    'author_email'
]
