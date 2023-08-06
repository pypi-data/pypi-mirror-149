"""Модуль архиватора баз данных SQLite."""

import os
import subprocess
import shlex
import logging

from msbackup.backend_base import Base as BaseBackend


logger = logging.getLogger('msbackup')


def get_backend_kwargs(params):
    """Подготовка параметров для режима 'sqlite'."""
    kwargs = BaseBackend.get_common_backend_kwargs(params)
    BaseBackend.get_param(params, kwargs, 'sqlite_cmd')
    return kwargs


class Sqlite(BaseBackend):
    """Архиватор баз данных SQLite."""

    SECTION = 'Backend-SQLite'

    @classmethod
    def make_subparser(cls, subparsers):
        """Добавление раздела параметров командной строки для архиватора."""
        parser = subparsers.add_parser('sqlite')
        parser.set_defaults(get_backend_kwargs=get_backend_kwargs)
        parser.add_argument(
            '--sqlite-cmd',
            help='Command to run SQLite command-line shell.',
        )
        parser.add_argument(
            'source', nargs='*', metavar='DBNAME',
            help='Path to database file.')

    def __init__(self, config, *args, **kwargs):
        """Конструктор."""
        super().__init__(config, *args, **kwargs)
        self.suffix = '.gz' + (self.encryptor.suffix if self.encryptor else '')
        self.sqlite_cmd = shlex.split(kwargs.get('sqlite_cmd') or config.get(
            section=self.SECTION,
            option='SQLITE_COMMAND',
            fallback='/usr/bin/sqlite3',
        ))
        self.bakdb = None
        self.bakdb_file = None

    def source_name(self, source):
        """Имя источника архива."""
        return os.path.splitext(source)[0]

    def _backup(self, sources=None, **kwargs):
        """
        Архивация баз данных SQLite.

        :param source: Список источников для архивации.
        :type source: [str]
        :return: Количество ошибок.
        :rtype: int
        """
        if sources is None:
            raise AttributeError('source is not specified')
        error_count = 0
        for source in sources:
            output = self.outpath(os.path.basename(source))
            logger.info('Backup source "%s".', source)
            try:
                self.archive(
                    source=source,
                    output=output,
                )
            except subprocess.CalledProcessError as ex:
                logger.error(str(ex))
                error_count += 1
        return error_count

    def _archive(self, source, output=None, **kwargs):
        """
        Упаковка списка источников в файл архива.

        :param source: Путь к файлу БД SQLite.
        :type source: str
        :param output: Путь к файлу архива.
        :type output: str
        :return: Процесс упаковки файлов.
        :rtype: subprocess.Popen
        """
        self.bakdb = os.path.join(
            self.tmp_dir,
            os.path.basename(source),
        )
        logger.debug(
            'Dump source "%s" to temporary database "%s".',
            source, self.bakdb)
        cmd = self.sqlite_cmd.copy()
        cmd.extend([source, '.backup "{}"'.format(self.bakdb)])
        subprocess.check_call(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=self.stream_err,
        )
        if output is None:
            self.bakdb_file = open(self.bakdb, mode='rb')
            return self._compress_proc(
                in_stream=self.bakdb_file,
                out_stream=subprocess.PIPE,
            )
        else:
            with open(self.bakdb, mode='rb') as bakdb_file:
                with open(output, mode='wb') as out_file:
                    self._compress(
                        in_stream=bakdb_file,
                        out_stream=out_file,
                    )

    def _cleanup(self):
        """Удаление временных объектов."""
        if self.bakdb_file is not None:
            self.bakdb_file.close()
            self.bakdb_file = None
        if self.bakdb is not None and os.path.exists(self.bakdb):
            logger.debug('Remove temporary database "%s".', self.bakdb)
            os.remove(self.bakdb)
            self.bakdb = None
