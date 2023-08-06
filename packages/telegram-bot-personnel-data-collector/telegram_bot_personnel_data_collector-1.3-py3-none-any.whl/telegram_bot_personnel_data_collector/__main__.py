import os

from localisation import ServiceVocabulary
from session_cache import OpenSessions
from telegram import Service, handlers_register
from session_cache import background_expired_sessions_handler
from google_sheets import DB_AS_GoogleSheet
from utils import create_logger

logger = create_logger('Bot', 'DEBUG')


def main(*callback_list):
    try:
        OpenSessions.start()
        DB_AS_GoogleSheet.load(table_url=os.getenv('TABLE_URL'),
                               table_sheet=os.getenv('TABLE_SHEET'),
                               drive_folder_id=os.getenv('TABLE_FOLDER', None),
                               service_account_file=os.path.join(os.getenv('CREDENTIALS'), os.getenv('SECRET_FILE')))
        ServiceVocabulary.load()
        handlers_register(Service.dp)
        Service.start(start_up=callback_list)
    except KeyboardInterrupt:
        logger.info(f"User keyword interrupt")
    except Exception as e:
        logger.error(f"Unexpected: {e}")
    finally:
        Service.stop()


if __name__ == '__main__':
    main(background_expired_sessions_handler(Service.bot))
