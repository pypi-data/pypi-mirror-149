"""Archivers module."""

import shlex
import subprocess


class Tar(object):
    """Архиватор посредством утилиты tar."""

    def __init__(self, config, section='DEFAULT', **kwargs):
        """
        Конструктор.

        :param config: Конфигурация.
        :type config: :class:`ConfigParser.RawConfigParser`
        :param encryptor: Шифровальщик архива.
        """
        cmd = kwargs.get('tar_cmd') or config.get(
            section, 'TAR_COMMAND', fallback='/bin/tar --gzip --warning=none')
        self.cmd = shlex.split(cmd)
        self.suffix = config.get(section, 'TAR_SUFFIX', fallback='.tar.gz')

    def pack(self, source, output=None, base_dir=None, **kwargs):
        """
        Архивация файлов или папки.

        :param source: Источник или список источников для архивации.
        :type source: str или [str]
        :param output: Путь к файлу архива.
        :type output: str
        :param base_dir: Путь к папке с архивами.
        :type base_dir: str
        :param kwargs: Дополнительные параметры для tar.
        :type kwargs: [str]
        :return: Процесс упаковки файлов.
        :rtype: subprocess.Popen
        """
        sources = [source] if isinstance(source, str) else source
        params = self.cmd.copy()
        params.append('--create')
        if output is not None:
            params.extend(['--file', output])
            kwargs['stdout'] = kwargs.get('stdout') or subprocess.DEVNULL
        else:
            kwargs['stdout'] = subprocess.PIPE
        if base_dir is not None:
            params.extend(['-C', base_dir])
        if 'exclude' in kwargs:
            for ex in kwargs.pop('exclude'):
                params.append('--exclude={}'.format(ex))
        if 'exclude_from' in kwargs:
            for exf in kwargs.pop('exclude_from'):
                params.append('--exclude-from={}'.format(exf))
        params.extend(sources)
        if 'stderr' not in kwargs:
            kwargs['stderr'] = subprocess.PIPE
        if output is None:
            return subprocess.Popen(params, **kwargs)
        else:
            subprocess.check_call(params, **kwargs)


ARCHIVERS = {'tar': Tar}


def make_archiver(name, *args, **kwargs):
    """
    Фабрика архиватора.

    :param name: Имя архиватора.
    :type name: str
    :param config: Конфигурация.
    :type config: :class:`ConfigParser.RawConfigParser`
    :param encryptor: Шифровальщик.
    """
    if name not in ARCHIVERS:
        raise AttributeError('Unknown archiver: {}'.format(name))
    return ARCHIVERS[name](*args, **kwargs)
