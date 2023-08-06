"""Модуль архиваторов."""

from msbackup.backend_file import File
from msbackup.backend_svn import Subversion
from msbackup.backend_hg import Mercurial
from msbackup.backend_pg import PostgreSQL
from msbackup.backend_sqlite import Sqlite
from msbackup.backend_mongodb import MongoDB
from msbackup.backend_ldap import Ldap
from msbackup.backend_kvm import Kvm


BACKENDS = {
    'file': File,
    'hg': Mercurial,
    'svn': Subversion,
    'pg': PostgreSQL,
    'sqlite': Sqlite,
    'mongodb': MongoDB,
    'ldap': Ldap,
    'kvm': Kvm,
}
INIT_BACKENDS_LIST = [
    'file', 'hg', 'svn', 'pg', 'sqlite', 'mongodb', 'ldap', 'kvm',
]


def make_backend(name, *args, **kwargs):
    """
    Создание объекта архиватора.

    :param name: Имя архиватора.
    :type name: str
    :param config: Объект конфигурации архиватора.
    :type config: :class:`ConfigParser.RawConfigParser`
    """
    if name not in BACKENDS:
        raise AttributeError('Unknown back-end: {}'.format(name))
    return BACKENDS[name](*args, **kwargs)
