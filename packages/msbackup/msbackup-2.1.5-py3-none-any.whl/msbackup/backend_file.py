"""Модуль архиватора файлов и папок."""

import os
import subprocess
import logging

from msbackup.backend_base import Base as BaseBackend


logger = logging.getLogger('msbackup')


def get_backend_kwargs(params):
    """Подготовка параметров архиватора для режима 'file'."""
    kwargs = BaseBackend.get_common_backend_kwargs(params)
    BaseBackend.get_param(params, kwargs, 'archive_name')
    BaseBackend.get_param(params, kwargs, 'base_dir')
    return kwargs


class File(BaseBackend):
    """Архиватор файлов и папок."""

    SECTION = 'Backend-File'

    @classmethod
    def make_subparser(cls, subparsers):
        """Добавление раздела параметров командной строки для архиватора."""
        parser = subparsers.add_parser('file')
        parser.set_defaults(get_backend_kwargs=get_backend_kwargs)
        parser.add_argument(
            '-n', '--name', dest='archive_name', metavar='NAME',
            help='Name of archive file without extension.',
        )
        parser.add_argument(
            '-C', '--base-dir', dest='base_dir', metavar='DIR',
            help='Archiver will change to directory DIR.',
        )
        parser.add_argument(
            'source', nargs='*', metavar='PATH',
            help='Path to file or directory.')

    def __init__(self, config, *args, **kwargs):
        """Конструктор."""
        super().__init__(config, *args, **kwargs)
        # config file options
        self.base_dir = kwargs.get('base_dir') or config.get(
            section=self.SECTION,
            option='BASE_DIR',
            fallback=None,
        )
        a_name = kwargs.get('archive_name') or config.get(
            section=self.SECTION,
            option='ARCHIVE_NAME',
            fallback=None,
        )
        self.archive_name = os.path.basename(a_name) if a_name else None

    def _backup(self, sources=None, **kwargs):
        """
        Архивация файлов или папок.

        :param source: Список источников для архивации.
        :type source: [str]
        :return: Количество ошибок.
        :rtype: int
        """
        if sources is None:
            raise AttributeError('source is not specified')
        name = kwargs.get('archive_name', self.archive_name)
        if name is None:
            name = os.path.basename(sources[0])
        if name == '':
            name = os.uname().nodename
        output = self.outpath(source=name)
        base_dir = kwargs.get('base_dir', self.base_dir)
        try:
            self.archive(
                source=sources,
                output=output,
                base_dir=base_dir,
                exclude=[self.backup_dir],
            )
        except subprocess.CalledProcessError as ex:
            logger.error(str(ex))
            return 1
        return 0

    def _archive(self, source, output=None, **kwargs):
        """
        Упаковка списка источников в файл архива.

        :param source: Список источников для архивации.
        :type source: [str]
        :param output: Путь к файлу архива.
        :type output: str
        :return: Процесс упаковки файлов.
        :rtype: subprocess.Popen
        """
        params = {
            'source': source,
            'output': output,
            'stderr': self.stream_err,
        }
        ex = []
        if self.exclude is not None:
            ex.extend(self.exclude)
        if 'exclude' in kwargs:
            ex.extend(kwargs.pop('exclude'))
        if ex:
            params['exclude'] = ex
        params.update(kwargs)
        if self.exclude_from is not None:
            exclude_from = []
            for exf in self.exclude_from:
                exclude_from.append(self._relative_to_abs(exf))
            params['exclude_from'] = exclude_from
        return self.pack(**params)
