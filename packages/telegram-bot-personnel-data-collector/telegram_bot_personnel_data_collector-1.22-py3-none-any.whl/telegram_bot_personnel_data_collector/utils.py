import logging, os, sys
from abc import ABC, abstractmethod
from threading import RLock

import yaml


def get_error_info():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return file_name, exc_tb.tb_lineno


class Singleton:
    _instances = {}

    def __init__(self, class_):
        self._class_ = class_

    def __call__(self, *args, **kwargs):
        if self._class_ not in self._instances:
            self._instances[self._class_] = self._class_(*args, **kwargs)
        return self._instances[self._class_]


class threadsafety_dict(dict):
    def __init__(self, **kwargs):
        self._lock = kwargs.pop('lock', None) or RLock()
        super().__init__(**kwargs)

    @property
    def lock(self):
        return self._lock

    def __getitem__(self, item):
        with self._lock:
            return super().__getitem__(item)

    def __setitem__(self, key, value):
        with self._lock:
            super().__setitem__(key, value)

    def __delitem__(self, key):
        with self._lock:
            super().__delitem__(key)

    def __len__(self):
        with self._lock:
            return super().__len__()


def read_file(file):
    with open(file, 'r') as file:
        lines = file.readlines()
        text = '\n'.join(lines)
        return text


def load_yaml(file_path):
    with open(file_path, 'r') as reader:
        data = yaml.load(reader, yaml.FullLoader)
        return data


class YamlDataAbstract(dict, ABC):
    def __init__(self, yaml_file=None):
        if yaml_file:
            self._yaml_file = yaml_file

    def load(self, yaml_file=None):
        file = yaml_file or self._yaml_file
        assert file is not None, "Please provide Yaml file source"
        data = load_yaml(file)
        logging.info(f"File {file} loaded")
        logging.info(f"Data loaded\n\n{data}\n -------------------------")
        super().__init__(**data)


def create_logger(name, level=logging.INFO):
    logging.basicConfig(level=level,
                        format='[%(asctime)s][%(threadName)s : %(filename)s: %(lineno)d] %(levelname)s - %(message)s'
                        )
    _logger = logging.getLogger(name)
    _logger.info(f"DEBUG Level set: {level}")
    return _logger


class DBModel(ABC):

    @abstractmethod
    def set_person(self, **person_properties):
        """
        Adding personnel data entry
        If person username already existing - update entry

        :param person_properties:
        """
        pass

    @abstractmethod
    def is_person_exist(self, **person_properties):
        """
        Looking person entry by 'username'
        Return entry id or last free line number if not exist
        :param person_properties:
        """
        pass


__all__ = [
    'Singleton',
    'threadsafety_dict',
    'read_file',
    'load_yaml',
    'create_logger',
    'YamlDataAbstract',
    'DBModel',
    'get_error_info'
]
