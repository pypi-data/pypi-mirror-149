"""Модуль определения класса управления файлами блокировок."""

import os
import socket
import logging


logger = logging.getLogger('mabackup')


class FileLockAcquisitionError(Exception):
    """Ошибка получения блокировки файла."""


class FileLockReleaseError(Exception):
    """Ошибка освобождения блокировки файла."""


class Flock(object):
    """Класс управления файлами (pid) блокировок."""

    def __init__(self, path, debug=False):
        """Конструктор."""
        self.pid = os.getpid()
        self.host = socket.gethostname()
        self.path = path
        self.debug = debug

    def addr(self):
        """Получение адреса узла."""
        return '%d@%s' % (self.pid, self.host)

    def fddr(self):
        """Получить FDDR файла блокировки."""
        return '<%s %s>' % (self.path, self.addr())

    def pddr(self, lock):
        """Получить PDDR файла блокировки."""
        return '<%s %s@%s>' % (self.path, lock['pid'], lock['host'])

    def acquire(self):
        """Получение блокировки, возвращает self при успехе, иначе False."""
        if self.islocked():
            if self.debug:
                lock = self._readlock()
                logger.error('Previous lock detected: %s' % self.pddr(lock))
            return False
        try:
            with open(self.path, 'w') as fh:
                fh.write(self.addr())
            if self.debug:
                logger.debug('Acquired lock: %s' % self.fddr())
        except Exception:
            if os.path.isfile(self.path):
                try:
                    os.unlink(self.path)
                except Exception:  # pragma: no coverage
                    pass
            raise FileLockAcquisitionError(
                'Error acquiring lock: %s' % self.fddr())
        return self

    def release(self):
        """Освобождене блокировки, возврат self."""
        if self.ownlock():
            try:
                os.unlink(self.path)
                if self.debug:
                    logger.debug('Released lock: %s' % self.fddr())
            except Exception:
                raise FileLockReleaseError(
                    'Error releasing lock: %s' % self.fddr())
        return self

    def _readlock(self):
        """Чтение информации о блокировке."""
        try:
            lock = {}
            with open(self.path) as fh:
                data = fh.read().rstrip().split('@')
            lock['pid'] = int(data[0])
            lock['host'] = data[1]
            return lock
        except Exception:
            return {'pid': 8**10, 'host': ''}

    def islocked(self):
        """Проверка наличия блокировки."""
        try:
            lock = self._readlock()
            os.kill(lock['pid'], 0)
            return (lock['host'] == self.host)
        except Exception:
            return False

    def ownlock(self):
        """Проверка владения блокировкой."""
        lock = self._readlock()
        return (self.fddr() == self.pddr(lock))

    def __del__(self):
        """Деструктор."""
        self.release()
