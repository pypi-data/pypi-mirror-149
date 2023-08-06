import logging, os

from .utils import Singleton, YamlDataAbstract


logger = logging.getLogger(os.path.split(__file__)[-1])


@Singleton
class _configurations(YamlDataAbstract):
    Location = ''

    @property
    def get_admin_list(self):
        return self.get('admin_list')


Configurations: _configurations = _configurations()

__all__ = [
    'Configurations'
]
