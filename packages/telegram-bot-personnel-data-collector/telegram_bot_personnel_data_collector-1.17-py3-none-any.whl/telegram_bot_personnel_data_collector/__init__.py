import os


from telegram_bot_personnel_data_collector import arg_parse
from telegram_bot_personnel_data_collector import telegram
from telegram_bot_personnel_data_collector import google_sheets
from telegram_bot_personnel_data_collector import localisation
from telegram_bot_personnel_data_collector import session_cache
from telegram_bot_personnel_data_collector import utils

__doc__ = """
Documents: https://core.telegram.org/bots/api
"""

version = '1.17'
author = 'Dmitry Oguz'
author_email = 'doguz2509@gmail.com'

PACKAGE_DIR = r'/opt'


__all__ = [
    'PACKAGE_DIR',
    'version',
    'author',
    'author_email'
]

