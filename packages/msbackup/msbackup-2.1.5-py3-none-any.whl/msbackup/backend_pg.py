"""Модуль архиватора баз данных PostgreSQL."""

import os
import sys
import subprocess
import shlex
import logging

from msbackup import utils
from msbackup.backend_base import Base as BaseBackend


logger = logging.getLogger('msbackup')


def get_backend_kwargs(params):
    """Подготовка параметров для режима 'pg'."""
    kwargs = BaseBackend.get_common_backend_kwargs(params)
    BaseBackend.get_param(params, kwargs, 'host')
    BaseBackend.get_param(params, kwargs, 'port')
    BaseBackend.get_param(params, kwargs, 'username')
    BaseBackend.get_param(params, kwargs, 'format')
    BaseBackend.get_param(params, kwargs, 'schema_only')
    BaseBackend.get_param(params, kwargs, 'psql_cmd')
    BaseBackend.get_param(params, kwargs, 'pgdump_cmd')
    return kwargs


class PostgreSQL(BaseBackend):
    """Архиватор баз данных PostgreSQL."""

    SECTION = 'Backend-PostgreSQL'

    FORMAT_NONE = 0  # Формат архива не задан.
    FORMAT_PLAIN = 1  # Полный архив БД в текстовом формате.
    FORMAT_CUSTOM = 2  # Полный архив БД в сжатом формате.

    FORMAT_MAP = {
        'plain': FORMAT_PLAIN,
        'custom': FORMAT_CUSTOM,
        'default': FORMAT_NONE,
    }
    MODE_NONE = 0  # Запрет архивирования БД.
    MODE_SCHEMA = 1  # Архивировать только схему БД.
    MODE_FULL = 2  # Полный архив БД.

    @classmethod
    def make_subparser(cls, subparsers):
        """Добавление раздела параметров командной строки для архиватора."""
        parser = subparsers.add_parser('pg')
        parser.set_defaults(get_backend_kwargs=get_backend_kwargs)
        parser.add_argument('-H', '--host', help='PostgreSQL hostname.')
        parser.add_argument('-p', '--port', help='PostgreSQL port number.')
        parser.add_argument('-U', '--username', help='PostgreSQL username.')
        parser.add_argument(
            '-f', '--format', choices=cls.FORMAT_MAP,
            help='Backup format (default: plain).',
        )
        parser.add_argument(
            '-s', '--schema-only',
            help='List of databases to only backup schema.',
        )
        parser.add_argument(
            '--psql-cmd',
            help='Command to run PostgreSQL shell (default: /usr/bin/psql).',
        )
        parser.add_argument(
            '--pgdump-cmd',
            help=('Command to run PostgreSQL dump util '
                  '(default: /usr/bin/pg_dump).'),
        )
        parser.add_argument(
            'source', nargs='*', metavar='DBNAME', help='Name of database.')

    def __init__(self, config, **kwargs):
        """
        Конструктор.

        :param config: Конфигурация.
        :type config: :class:`ConfigParser.RawConfigParser`
        :param out: Поток вывода информационных сообщений.
        :param err: Поток вывода сообщений об ошибках.
        :param encryptor: Имя шифровальщика.
        :type encryptor: str
        """
        super().__init__(config, **kwargs)
        self._init_options(config, kwargs)
        # psql_cmd
        self.psql_cmd = shlex.split(kwargs.get('psql_cmd') or config.get(
            section=self.SECTION,
            option='PSQL_COMMAND',
            fallback='/usr/bin/psql',
        ))
        # pgdump_cmd
        self.pgdump_cmd = shlex.split(kwargs.get('pgdump_cmd') or config.get(
            section=self.SECTION,
            option='PGDUMP_COMMAND',
            fallback='/usr/bin/pg_dump',
        ))
        # exclude_from
        if self.exclude_from is not None:
            exclude = self.exclude if self.exclude is not None else []
            for exf in self.exclude_from:
                exclude.extend(self._load_exclude_file(exf))
            self.exclude = exclude if len(exclude) > 0 else None
            self.exclude_from = None

    def _init_options(self, config, kwargs):
        """Обработка параметров."""
        self.host = kwargs.get('host') or config.get(
            section=self.SECTION, option='HOST', fallback=None)
        self.port = kwargs.get('port') or config.get(
            section=self.SECTION, option='PORT', fallback=None)
        self.username = kwargs.get('username') or config.get(
            section=self.SECTION,
            option='USERNAME',
            fallback=None,
        )
        format_name = kwargs.get('format') or config.get(
            section=self.SECTION, option='BACKUP_FORMAT', fallback='plain')
        if format_name not in self.FORMAT_MAP:
            raise AttributeError('Invalid backup format name: %s' % format_name)
        self.format = self.FORMAT_MAP[format_name]
        # schema_only_list
        self.schema_only_list = []
        lst = utils.dequote(kwargs.get('schema_only') or config.get(
            section=self.SECTION,
            option='SCHEMA_ONLY_LIST',
            fallback='',
        ))
        if lst:
            self.schema_only_list.extend(lst.split(' '))

    def outpath(self, name, **kwargs):
        """
        Формирование имени файла с архивом.

        :param name: Имя файла архива без расширения.
        :type name: str
        :param mode: Режим архивации базы данных.
        :type mode: int
        :return: Полный путь к файлу с архивом.
        :rtype: str
        """
        fname = name
        if kwargs.get('mode', self.MODE_NONE) == self.MODE_SCHEMA:
            fname += '_SCHEMA.sql'
            fname += self.compressor_suffix
        elif self.format == self.FORMAT_PLAIN:
            fname += '.sql'
            fname += self.compressor_suffix
        elif self.format == self.FORMAT_CUSTOM:
            fname += '.custom'
        else:
            fname += self.compressor_suffix
        if self.encryptor is not None:
            fname += self.encryptor.suffix
        return os.path.join(self.backup_dir, name, fname)

    def backup_info(self, mode):
        """Текстовое описание режима архивации базы данных."""
        if mode == self.MODE_SCHEMA:
            return 'Schema-only'
        elif self.format == self.FORMAT_PLAIN:
            return 'Plain'
        elif self.format == self.FORMAT_CUSTOM:
            return 'Custom'
        return 'Default'

    def _backup(self, sources=None, **kwargs):
        """
        Архивация баз данных PostgreSQL на заданном узле.

        :param sources: Список имён баз данных для архивации.
        :type sources: [str]
        :param base_dir: Путь к папке с источниками (игнорируется).
        :type base_dir: str
        :return: Количество ошибок.
        :rtype: int
        """
        dblist = sources if sources is not None else self.dblist(**kwargs)
        error_count = 0
        for database in dblist:
            if self.exclude is not None and database in self.exclude:
                logger.debug('Database "%s" in exclude list - skipped.',
                             database)
                continue
            mode = (self.MODE_SCHEMA if database in self.schema_only_list
                    else self.MODE_FULL)
            logger.info(
                '%s backup database "%s".',
                self.backup_info(mode), database,
            )
            try:
                self.archive(
                    source=database,
                    output=self.outpath(name=database, mode=mode),
                    mode=mode,
                    **kwargs,
                )
            except subprocess.CalledProcessError as ex:
                error_count += 1
                logger.error(str(ex))
        return error_count

    def _archive(self, source, output=None, **kwargs):
        """
        Архивация одной базы данных PostgreSQL.

        :param source: Имя базы данных.
        :type source: str
        :param output: Путь к файлу архива.
        :type output: str
        :return: Процесс упаковки файлов.
        :rtype: subprocess.Popen
        """
        mode = kwargs.pop('mode', self.MODE_NONE)
        logger.debug('Dump database "%s".', source)
        return self._dump_proc(
            database=source,
            mode=mode,
            output=output,
            **kwargs,
        )

    def dblist(self, **kwargs):
        """
        Список имён баз данных.

        :return: Список имён всех баз данных.
        :rtype: [str]
        """
        logger.debug('Get list of databases.')
        params = self.psql_cmd.copy()
        if self.host or 'host' in kwargs:
            params.append('--host={}'.format(
                kwargs.get('host', self.host)))
        if self.port or 'port' in kwargs:
            params.append('--port={}'.format(
                kwargs.get('port', self.port)))
        if self.username or 'username' in kwargs:
            params.append('--username={}'.format(
                kwargs.get('username', self.username)))
        params.append('--no-password')
        params.append('--no-align')
        params.append('--tuples-only')
        params.append('-c')
        params.append('SELECT datname '
                      'FROM pg_database '
                      'WHERE NOT datistemplate '
                      'ORDER BY datname;')
        params.append('postgres')
        out = subprocess.check_output(params)
        databases = out.decode(sys.getdefaultencoding()).splitlines()
        logger.debug('Found databases: %s.', str(databases))
        return databases

    def _dump_params(self, database, mode, output=None, **kwargs):
        """
        Подготовка процесса создания архива базы данных PostgreSQL.

        :param database: Имя базы данных.
        :type database: str
        :param mode: Режим архивации базы данных.
        :type mode: int
        :param output: Путь к файлу архива.
        :type output: str
        """
        params = self.pgdump_cmd.copy()
        if mode == self.MODE_SCHEMA or self.format == self.FORMAT_PLAIN:
            params.append('--format=p')
        elif self.format == self.FORMAT_CUSTOM:
            params.append('--format=c')
        if mode == self.MODE_SCHEMA:
            params.append('--schema-only')
        if self.host or 'host' in kwargs:
            params.append('--host={}'.format(
                kwargs.get('host', self.host)))
        if self.port or 'port' in kwargs:
            params.append('--port={}'.format(
                kwargs.get('port', self.port)))
        if self.username or 'username' in kwargs:
            params.append('--username={}'.format(
                kwargs.get('username', self.username)))
        params.append('--no-password')
        if output is not None:
            params.append('--file={}'.format(output))
        params.append('--compress=9')
        params.append(database)
        return params

    def _dump_proc(self, *args, **kwargs):
        """
        Подготовка процесса создания архива базы данных PostgreSQL.

        :param output: Путь к файлу с архивом.
        :type output: str
        """
        popen_kwargs = {'stderr': self.stream_err}
        params = self._dump_params(*args, **kwargs)
        logger.debug('Dump database with params: %s', params)
        if 'output' in kwargs and kwargs['output'] is not None:
            subprocess.check_call(params, **popen_kwargs)
        else:
            popen_kwargs['stdout'] = subprocess.PIPE
            return subprocess.Popen(params, **popen_kwargs)
