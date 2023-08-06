"""Модуль шифровальщиков."""

import subprocess
import logging
import shlex


logger = logging.getLogger('msbackup')


class Gpg(object):
    """Шифровальщик посредством утилиты GnuPG."""

    def __init__(self, config, section='DEFAULT', **kwargs):
        """
        Конструктор.

        :param config: Конфигурация.
        :type config: :class:`ConfigParser.RawConfigParser`
        """
        cmd = kwargs.get('gpg_cmd') or config.get(
            section, 'GPG_COMMAND', fallback='/usr/bin/gpg')
        self.cmd = shlex.split(cmd)
        self.cmd.extend(['--quiet', '--batch'])
        self.recipient = kwargs.get('gpg_recipient') or config.get(
            section, 'GPG_RECIPIENT', fallback=None)
        self.suffix = config.get(
            section, 'GPG_SUFFIX', fallback='.gpg')
        self.stderr = kwargs.get('err', subprocess.PIPE)

    def encrypt(self, output, source=None, in_stream=None):
        """
        Шифрование файла.

        :param source: Путь к шифруемому файлу.
        :type source: str
        :param output: Путь к зашифрованному файлу.
        :type output: str
        :param compress_level: Уровень сжатия зашифрованного файла.
        :type compress_level: int
        """
        params = self.cmd.copy()
        params.append('--output')
        params.append(output)
        if self.recipient is not None:
            params.append('--recipient')
            params.append(self.recipient)
        else:
            params.append('--default-recipient-self')
        params.append('--encrypt')
        call_kwargs = {
            'stdout': subprocess.DEVNULL,
            'stderr': self.stderr,
        }
        if source is not None:
            params.append(source)
        elif in_stream is not None:
            call_kwargs['stdin'] = in_stream
        else:
            raise AttributeError(
                'Gpg.encrypt() source or in_stream must be not None'
            )
        logger.debug('Run encrypt command: "%s".', ' '.join(params))
        subprocess.check_call(params, **call_kwargs)


# Encryptors map.
ENCRYPTORS = {
    'gpg': Gpg,  # Use gnupg encryptor.
}


def make_encryptor(name, *args, **kwargs):
    """
    Фабрика шифровальщика.

    :param name: Имя шифровальщика.
    :type name: str
    :param config: Конфигурация.
    :type config: :class:`ConfigParser.RawConfigParser`
    """
    if name not in ENCRYPTORS:
        raise AttributeError('Unknown encryptor: {}'.format(name))
    return ENCRYPTORS[name](*args, **kwargs)
