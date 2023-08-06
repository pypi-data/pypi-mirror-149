from telegram_bot_personnel_data_collector.utils import Singleton


@Singleton
class _configurations:
    Location = ''


Configurations = _configurations()

__all__ = [
    'Configurations'
]
