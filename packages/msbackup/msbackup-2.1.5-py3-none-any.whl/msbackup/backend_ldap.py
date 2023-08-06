"""Модуль архиватора базы данных OpenLDAP."""

import os
import subprocess
import tempfile
import shutil
import shlex
import logging

from msbackup.backend_base import Base as BaseBackend


logger = logging.getLogger('msbackup')


def get_backend_kwargs(params):
    """Подготовка параметров для режима 'ldap'."""
    kwargs = BaseBackend.get_common_backend_kwargs(params)
    BaseBackend.get_param(params, kwargs, 'archive_name')
    BaseBackend.get_param(params, kwargs, 'slapcat_cmd')
    BaseBackend.get_param(params, kwargs, 'ldap_conf_dir')
    return kwargs


class Ldap(BaseBackend):
    """Архиватор базы данных OpenLDAP."""

    SECTION = 'Backend-LDAP'

    @classmethod
    def make_subparser(cls, subparsers):
        """Добавление раздела параметров командной строки для архиватора."""
        parser = subparsers.add_parser('ldap')
        parser.set_defaults(get_backend_kwargs=get_backend_kwargs)
        parser.add_argument(
            '-n', '--name', dest='archive_name', metavar='NAME',
            help='Name of archive file without extension.',
        )
        parser.add_argument(
            '--slapcat-cmd',
            help=('Command to run OpenLDAP command-line util '
                  '(default: /usr/sbin/slapcat).'),
        )
        parser.add_argument(
            '--ldap-conf-dir',
            help=('Path to OpenLDAP config directory '
                  '(default: /etc/ldap/slapd.d).'),
        )
        parser.add_argument(
            'source', nargs='+', metavar='BASEDN',
            help='Base DN for backup.',
        )

    def __init__(self, config, *args, **kwargs):
        """Конструктор."""
        super().__init__(config, *args, **kwargs)
        a_name = kwargs.get('archive_name') or config.get(
            section=self.SECTION,
            option='ARCHIVE_NAME',
            fallback=None,
        )
        self.archive_name = os.path.basename(a_name) if a_name else None
        cmd = shlex.split(kwargs.get('slapcat_cmd') or config.get(
            section=self.SECTION,
            option='SLAPCAT_COMMAND',
            fallback='/usr/sbin/slapcat',
        ))
        ldap_conf_dir = kwargs.get('ldap_conf_dir') or config.get(
            section=self.SECTION,
            option='LDAP_CONF_DIR',
            fallback='/etc/ldap/slapd.d',
        )
        cmd.extend(['-F', ldap_conf_dir])
        self.slapcat_cmd = cmd
        self.tmpdir = None

    def _backup(self, sources=None, **kwargs):
        """
        Архивация баз данных OpenLDAP.

        :param source: Список источников для архивации.
        :type source: [str]
        :return: Количество ошибок.
        :rtype: int
        """
        name = kwargs.get('archive_name', self.archive_name)
        if name is None:
            name = os.uname().nodename
        output = self.outpath(name)
        try:
            self.archive(
                source=sources,
                output=output,
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
        self.tmpdir = tempfile.mkdtemp(dir=self.tmp_dir)
        logger.debug('Created temporary directory "%s".', self.tmpdir)
        conf_file = os.path.join(self.tmpdir, 'ldap.config.ldif')
        params = self.slapcat_cmd.copy()
        params.extend(['-b', 'cn=config', '-l', conf_file])
        logger.debug('Read LDAP configuration to "%s".', conf_file)
        subprocess.check_call(
            params,
            stdout=subprocess.DEVNULL,
            stderr=self.stream_err,
        )
        pack_files = [os.path.basename(conf_file)]
        for src in source:
            name = '.'.join(
                item.replace('dc=', '') for item in src.split(','))
            data_file = os.path.join(self.tmpdir, '{}.ldif'.format(name))
            pack_files.append(os.path.basename(data_file))
            params = self.slapcat_cmd.copy()
            params.extend(['-b', src, '-l', data_file])
            logger.debug('Read domain "%s" to "%s".', name, data_file)
            subprocess.check_call(
                params,
                stdout=subprocess.DEVNULL,
                stderr=self.stream_err,
            )
        return self.pack(
            source=pack_files,
            base_dir=self.tmpdir,
            stderr=self.stream_err,
            output=output,
            **kwargs,
        )

    def _cleanup(self):
        """Удаление временных объектов."""
        if self.tmpdir is not None:  # pragma: no coverage
            logger.debug('Remove temporary directory "%s".', self.tmpdir)
            shutil.rmtree(self.tmpdir, ignore_errors=True)
            self.tmpdir = None
