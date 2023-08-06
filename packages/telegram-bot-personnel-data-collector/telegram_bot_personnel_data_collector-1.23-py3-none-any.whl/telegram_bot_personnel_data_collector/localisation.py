import logging
import os
import re

from .configurations import Configurations
from .utils import Singleton, YamlDataAbstract


logger = logging.getLogger(os.path.split(__file__)[-1])


class FormatException(AssertionError):
    pass


class TranslateException(AssertionError):
    pass


def FormatHandler(item: dict, value):
    formatter = item.get('formatter', None)
    if formatter is None:
        return
    _result = []

    for format_item in formatter:
        try:
            assert re.match(format_item.get('regex', None), value)
        except AssertionError:
            _result.append(format_item.get('error_text', None))

    if len(_result) > 0:
        raise FormatException("\n".join(_result))


def TranslateHandler(item: dict, value):
    translator = item.get('translator', None)
    if translator is None:
        return value

    for english_name, variants in translator.items():
        if value.lower() == english_name:
            return str(english_name).capitalize()
        if value.lower() in [v.lower() for v in variants]:
            return str(english_name).capitalize()
    raise TranslateException(f"Cannot translate '{value}'")


@Singleton
class _vocabulary(YamlDataAbstract):
    def get_path(self, *path_items):
        path_i = path_items[:-1]
        lang = path_items[-1]
        temp_result = self
        for item in path_i:
            temp_result = temp_result[item]
            assert temp_result, f"Cannot resolve {path_items}"
        if isinstance(temp_result, (list, tuple)):
            temp_result = temp_result[lang]
        elif isinstance(temp_result, dict):
            temp_result = temp_result.get(lang, None) or temp_result.get('en')
        return temp_result

    def get_picture(self, *path_items):
        try:
            _path = self.get_path(*path_items)
            return os.path.normpath(os.path.join(Configurations.Location, _path))
        except AssertionError:
            return None


@Singleton
class _config(YamlDataAbstract):
    pass


ServiceVocabulary: _vocabulary = _vocabulary()


__all__ = [
    'ServiceVocabulary',
    'FormatHandler',
    'FormatException',
    'TranslateHandler',
    'TranslateException'
]
