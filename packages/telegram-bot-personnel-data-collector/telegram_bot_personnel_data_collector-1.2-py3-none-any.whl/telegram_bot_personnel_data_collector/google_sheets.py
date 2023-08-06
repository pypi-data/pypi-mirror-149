import os.path, logging

from google_sheets_lib import GoogleSheets

from utils import Singleton, DBModel


logger = logging.getLogger(os.path.split(__file__)[-1])


@Singleton
class _google(GoogleSheets, DBModel):
    def __init__(self, table_url, table_sheet, drive_folder_id=None, logging_level: str = 'INFO', service_account_file: str = None,
                 credentials=None):
        GoogleSheets.__init__(self, drive_folder_id, logging_level, service_account_file, credentials)
        self._sheet_name = table_sheet
        self._work_book = self.set_sheet(url=table_url)
        self._column_map = None
        logger.info(f"Sheet {self._sheet_name} ready")

    @property
    def WorkSheet(self):
        return self._work_book.sheet[self._sheet_name]

    def set_person(self, **person_properties):
        row_offset = self.is_person_exist(**person_properties)
        try:
            self.update_row_by_header([dict(Num=row_offset-1, **person_properties)], header_row=1, row_offset=row_offset)
        except Exception as e:
            logger.error(f"Cannot write person entry: {person_properties}:\n{e}")
            raise

    def is_person_exist(self, **person_properties) -> int:
        last_index = 0
        header = self.get_row(1)
        for index, user_id in enumerate(self.get_column(header.index('user_id') + 1)):
            last_index = index
            if str(person_properties.get('user_id')) == str(user_id):
                return last_index + 1
        return last_index + 2


DB: _google = _google(table_url=os.getenv('TABLE_URL'),
                      table_sheet=os.getenv('TABLE_SHEET'),
                      drive_folder_id=os.getenv('TABLE_FOLDER', None),
                      service_account_file=os.path.join(os.getenv('CREDENTIALS'), os.getenv('SECRET_FILE')))


__all__ = [
    'DB'
]


if __name__ == '__main__':
    try:
        DB.add_person()

    except Exception as e:
        print(f"{e}")





