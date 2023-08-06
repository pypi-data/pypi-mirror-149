"""Модуль базового класса всех архиваторов."""

import os
import logging
import tempfile
import stat
import sys
import glob
import uuid
import shutil
import getpass
import subprocess
import shlex
import abc

from msbackup import utils, archive, encrypt


logger = logging.getLogger('msbackup')


class Base(metaclass=abc.ABCMeta):
    """Базовый класс архиваторов."""

    BACKUP_DIR_PERMISSIONS = (
        stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP |
        stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
    )
    ARCHIVE_PERMISSIONS = (
        stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP
    )

    @classmethod
    def get_param(cls, params, kwargs, name, validator=None):
        """Извлечение параметра из объекта."""
        def is_not_None(v):
            return v is not None
        if validator is None:
            validator = is_not_None
        value = getattr(params, name)
        if validator(value):
            kwargs[name] = value

    @classmethod
    def get_common_backend_kwargs(cls, params):
        """Извлечение общих параметров конструктора движка."""
        kwargs = {}
        cls.get_param(params, kwargs, 'backup_dir')
        cls.get_param(params, kwargs, 'archive_mode')
        cls.get_param(params, kwargs, 'tmp_dir')
        cls.get_param(params, kwargs, 'rotate')
        cls.get_param(params, kwargs, 'archiver')
        cls.get_param(params, kwargs, 'encrypt', validator=lambda v: v is True)
        cls.get_param(params, kwargs, 'encryptor')
        cls.get_param(params, kwargs, 'exclude')
        cls.get_param(params, kwargs, 'exclude_from')
        cls.get_param(params, kwargs, 'compressor_cmd')
        cls.get_param(params, kwargs, 'tar_cmd')
        cls.get_param(params, kwargs, 'gpg_cmd')
        cls.get_param(params, kwargs, 'gpg_recipient')
        cls.get_param(params, kwargs, 'owner_group')
        return kwargs

    @classmethod
    def make_options(cls, parser):
        """Добавление параметров командной строки."""
        archivers = sorted([item for item in archive.ARCHIVERS])
        encryptors = sorted([item for item in encrypt.ENCRYPTORS])
        parser.add_argument(
            '-c', '--config', metavar='FILE',
            help='Path to config file.',
        )
        parser.add_argument(
            '-b', '--backup-dir', dest='backup_dir',
            help='Path to archive directory (current by default).',
        )
        parser.add_argument(
            '-m', '--archive-mode', dest='archive_mode',
            choices=['IN_PLACE', 'IN_TMP_DIR'],
            type=lambda value: value.replace('-', '_').upper(),
            help='Mode for creating an archive file.',
        )
        parser.add_argument(
            '-t', '--tmp-dir',
            help='Folder path for temporary files.'
        )
        parser.add_argument(
            '-a', '--archiver', choices=archivers,
            help='Name of file archiver.',
        )
        parser.add_argument(
            '-g', '--encrypt', action='store_true',
            help='Encryption enabled.',
        )
        parser.add_argument(
            '-E', '--encryptor', choices=encryptors,
            help='Name of file encryptor.',
        )
        parser.add_argument(
            '-x', '--exclude', action='append', metavar='PATTERN',
            help='Exclude files defined by the PATTERN.',
        )
        parser.add_argument(
            '-X', '--exclude-from', dest='exclude_from',
            action='append', metavar='FILE',
            help='Exclude files defined in FILE.',
        )
        parser.add_argument(
            '-r', '--rotate', type=int,
            help='Number of archive files to be rotated.',
        )
        parser.add_argument(
            '-C', '--compressor-cmd',
            help='Command to run compressor (default: /bin/gzip -q9).',
        )
        parser.add_argument(
            '-T', '--tar-cmd',
            help='Command to run tar (default: /bin/tar --gzip).',
        )
        parser.add_argument(
            '-G', '--gpg-cmd',
            help='Command to run gnupg (default: /usr/bin/gpg).',
        )
        parser.add_argument(
            '-R', '--gpg-recipient',
            help='The recipient of the encrypted archive.',
        )
        parser.add_argument(
            '-O', '--owner-group',
            help='Group ownership of files and folders.',
        )
        return parser.add_subparsers(
            dest='backend',
            title='Back-end name',
        )

    @classmethod
    def validate_params(cls, parser, params):
        """Проверка параметров."""
        if params.backend is None:
            parser.error(
                'the following arguments are required: Back-end')

    def __init__(self, config, **kwargs):
        """
        Конструктор.

        :param config: Конфигурация.
        :type config: :class:`ConfigParser.RawConfigParser`
        """
        self.encoding = sys.getdefaultencoding()
        # Config
        if hasattr(config, 'config_file_path'):
            self.config_file_dir = os.path.dirname(
                getattr(config, 'config_file_path'))
        else:
            self.config_file_dir = None
        self.stream_err = kwargs.get('err') or sys.stderr
        self._init_base_options(config, kwargs)
        self._init_encryptor(config, kwargs)
        self._init_archiver(config, kwargs)
        self._init_exclude(config, kwargs)
        self._init_compressor(config, kwargs)

    def _init_base_options(self, config, kwargs):
        """Проверка простых параметров."""
        backup_user = config.get(self.SECTION, 'BACKUP_USER', fallback=None)
        if backup_user is not None and getpass.getuser() != backup_user:
            raise RuntimeError(
                'This program must be run as {}. Exiting.'.format(backup_user)
            )
        # source
        source = config.get(self.SECTION, 'SOURCE', fallback=None)
        self.source = source.split(' ') if source is not None else None
        # --backup-dir
        backup_dir = kwargs.get('backup_dir') or config.get(
            self.SECTION, 'BACKUP_DIR', fallback=None)
        if backup_dir is None or len(backup_dir) == 0:
            raise AttributeError('BACKUP_DIR is not configured')
        if not os.path.isabs(backup_dir):
            base_dir = config.get('DEFAULT', 'BACKUP_DIR', fallback=None)
            if base_dir is not None:
                backup_dir = os.path.join(base_dir, backup_dir)
        self.backup_dir = os.path.abspath(backup_dir)
        # --rotate
        self.rotate = kwargs.get('rotate') or config.getint(
            self.SECTION, 'ROTATE', fallback=0,
        )
        # --archive-mode
        self.archive_mode = kwargs.get('archive_mode') or config.get(
            self.SECTION, 'ARCHIVE_MODE', fallback='IN_PLACE',
        )
        # --tmp-dir
        self.tmp_dir = kwargs.get('tmp_dir') or config.get(
            self.SECTION, 'TMP_DIR', fallback=tempfile.gettempdir(),
        )
        # --owner-group
        self.owner_group = kwargs.get('owner_group') or config.get(
            self.SECTION, 'OWNER_GROUP', fallback=None,
        )

    def _init_encryptor(self, config, kwargs):
        """Настройка шифровальщика."""
        self.encrypt_enabled = kwargs.get(
            'encrypt', False,
        ) or config.getboolean(self.SECTION, 'ENCRYPT', fallback=False)
        self.encryptor = None
        if not self.encrypt_enabled:
            return
        encryptor_name = kwargs.get('encryptor') or config.get(
                self.SECTION, 'ENCRYPTOR', fallback=None)
        if encryptor_name is None:
            return
        self.encryptor = encrypt.make_encryptor(
            encryptor_name,
            config=config,
            section=self.SECTION,
            **kwargs,
        )

    def _init_archiver(self, config, kwargs):
        """Настройка архиватора."""
        archiver_name = kwargs.get('archiver') or config.get(
            self.SECTION,
            'ARCHIVER',
            fallback='tar',
        )
        self.archiver = archive.make_archiver(
            name=archiver_name,
            config=config,
            section=self.SECTION,
            **kwargs,
        )
        suffix = self.archiver.suffix
        if self.encryptor is not None:
            suffix += self.encryptor.suffix
        self.suffix = suffix
        self.progress_suffix = config.get(
            self.SECTION,
            'PROGRESS_SUFFIX',
            fallback='.in_progress',
        )

    def _init_exclude(self, config, kwargs):
        """Настрока исключений."""
        # EXCLUDE
        exclude = kwargs.get('exclude', [])
        if len(exclude) == 0:
            exclude_conf = config.get(self.SECTION, 'EXCLUDE', fallback=None)
            if exclude_conf is not None:
                exclude.extend(utils.dequote(exclude_conf).split(','))
        self.exclude = exclude if len(exclude) > 0 else None
        # EXCLUDE_FROM
        exclude_from = kwargs.get('exclude_from', [])
        if len(exclude_from) == 0:
            exclude_from_conf = config.get(
                self.SECTION,
                'EXCLUDE_FROM',
                fallback=None,
            )
            if exclude_from_conf is not None:
                for exf in utils.dequote(exclude_from_conf).split(','):
                    exf = utils.dequote(exf)
                    if exf == '':
                        continue
                    exclude_from.append(exf)
        self.exclude_from = exclude_from if len(exclude_from) > 0 else None

    def _init_compressor(self, config, kwargs):
        """Настройка компрессора."""
        compressor_cmd = kwargs.get('compressor_cmd') or config.get(
            section=self.SECTION,
            option='COMPRESSOR_COMMAND',
            fallback='/bin/gzip -q9',
        )
        self.compressor_cmd = shlex.split(compressor_cmd)
        self.compressor_suffix = config.get(
            section=self.SECTION,
            option='COMPRESSOR_SUFFIX',
            fallback='.gz',
        )

    def _relative_to_abs(self, file_path):
        """Преобразование относительного пути в абсолютный."""
        if os.path.isabs(file_path):
            return file_path
        if self.config_file_dir is None:
            return file_path
        return os.path.join(self.config_file_dir, file_path)

    def _load_exclude_file(self, filepath):
        """Загрузка файла с шаблонами исключения из архива в список строк."""
        exclude = []
        with open(self._relative_to_abs(filepath), 'r') as ex_file:
            for line in ex_file.readlines():
                exv = utils.dequote(line.strip())
                if exv != '':
                    exclude.append(exv)
        return exclude

    def _compress(self, in_stream, out_stream, **kwargs):
        """Сжатие потока in_stream в выходной поток out_stream."""
        subprocess.check_call(
            self.compressor_cmd,
            stdin=in_stream,
            stdout=out_stream,
            stderr=self.stream_err,
            **kwargs,
        )

    def _compress_proc(self, in_stream, out_stream, **kwargs):
        """Сжатие потока in_stream в выходной поток out_stream."""
        return subprocess.Popen(
            self.compressor_cmd,
            stdin=in_stream,
            stdout=out_stream,
            stderr=self.stream_err,
            **kwargs,
        )

    def source_name(self, source):
        """Имя источника архива."""
        return source

    def outpath(self, source, **kwargs):
        """
        Формирование имени файла с архивом.

        :param source: Имя файла архива без расширения.
        :type source: str
        :return: Полный путь к файлу с архивом.
        :rtype: str
        """
        return os.path.join(
            self.backup_dir,
            self.source_name(source),
            source + self.suffix,
        )

    def pack(self, *args, **kwargs):
        """Архивация файлов или папки."""
        return self.archiver.pack(*args, **kwargs)

    def backup(self, sources=None, **kwargs):
        """
        Архивация источников в заданную папку с архивами.

        :param sources: Список источников архива.
        :type sources: [str]
        :return: Код возврата.
        :rtype: int
        """
        logger.info('Backup started.')
        if not sources:
            sources = self.source
        if not os.path.exists(self.backup_dir):
            logger.info('Making backup directory in "%s".', self.backup_dir)
            try:
                os.makedirs(self.backup_dir, mode=self.BACKUP_DIR_PERMISSIONS)
                if self.owner_group is not None:
                    shutil.chown(self.backup_dir, group=self.owner_group)
            except Exception as ex:
                logger.critical(
                    'Error creating backup directory "%s": %s',
                    self.backup_dir,
                    str(ex),
                )
                raise
        if self.tmp_dir is not None and not os.path.exists(self.tmp_dir):
            logger.info('Making temporary directory in "%s".', self.tmp_dir)
            os.makedirs(self.tmp_dir, mode=self.BACKUP_DIR_PERMISSIONS)
        error_count = self._backup(sources=sources, **kwargs)
        if error_count != 0:
            logger.error('Errors occurred, number of errors: %d', error_count)
        logger.info('Backup complete.')
        return error_count

    def archive(self, source, output, **kwargs):
        """
        Упаковка источника в файл с архивом.

        При необхододимости выполняется ротация архивных файлов с таким же
        именем (без числового расширения), что и результирующий архив.

        :param source: Источник или список источников для архивации.
        :type source: str или [str]
        :param output: Путь к файлу с архивом.
        :type output: str
        :param base_dir: Путь к базовой папке источников.
        :type base_dir: str
        """
        output_dir = os.path.dirname(output)
        if not os.path.exists(output_dir):
            logger.debug('Making archive directory "%s".', output_dir)
            os.makedirs(output_dir, mode=self.BACKUP_DIR_PERMISSIONS)
            if self.owner_group is not None:
                shutil.chown(output_dir, group=self.owner_group)
        else:
            self._rotate(output)
        self._create_archive(source=source, output=output, **kwargs)

    def _create_archive(self, source, output, **kwargs):
        """Создание файла архива."""
        logger.debug('Create archive "%s".', output)
        try:
            if self.encrypt_enabled:
                self._create_encrypted_archive(
                    source=source,
                    output=output,
                    **kwargs,
                )
            else:
                self._archive(source=source, output=output, **kwargs)
        except Exception:
            if os.path.exists(output):
                os.remove(output)
            raise
        finally:
            self._cleanup()
        logger.debug('Change archive "%s" permissions.', output)
        os.chmod(output, self.ARCHIVE_PERMISSIONS)
        if self.owner_group is not None:
            shutil.chown(output, group=self.owner_group)
        logger.debug('Archive complete.')

    def _create_encrypted_archive(self, source, output, **kwargs):
        """Создание зашифрованного архива."""
        if self.archive_mode == 'IN_PLACE':
            proc = self._archive(source=source, **kwargs)
            self.encryptor.encrypt(
                output=output,
                in_stream=proc.stdout,
            )
        elif self.archive_mode == 'IN_TMP_DIR':
            tmpout = os.path.join(self.tmp_dir, uuid.uuid4().hex)
            try:
                self._archive(source=source, output=tmpout, **kwargs)
                self.encryptor.encrypt(output=output, source=tmpout)
            finally:
                if os.path.exists(tmpout):
                    os.remove(tmpout)
        else:
            raise AttributeError(
                'Unknown archive mode: %s' % self.archive_mode)

    def _rotate(self, output):
        """Ротация файлов с архивами."""
        output_dir = os.path.dirname(output)
        if self.rotate > 0 and os.path.isfile(output):
            logger.debug('Rotate archives in "%s" directory.', output_dir)
            pos = len(output) + 1
            rlist = []
            for archive_file in glob.iglob(output + '.*'):
                ext = archive_file[pos:]
                if ext.isdigit():
                    rlist.append((int(ext), archive_file))
            rlist.sort(key=lambda item: item[0], reverse=True)
            for item in rlist:
                num = item[0]
                if num < self.rotate:
                    shutil.move(item[1], '%s.%d' % (output, num + 1))
                elif num > self.rotate:
                    os.remove(item[1])
            os.rename(output, output + '.1')

    @abc.abstractmethod
    def _backup(self, sources=None, **kwargs):
        """
        Архивация набора источников.

        :param source: Список источников для архивации.
        :type source: [str]
        :return: Количество ошибок.
        :rtype: int
        """

    @abc.abstractmethod
    def _archive(self, source, output=None, **kwargs):
        """
        Упаковка источника в файл с архивом.

        :param source: Источник или список источников для архивации.
        :type source: str или [str]
        :param output: Путь к файлу архива.
        :type output: str
        :return: Процесс упаковки файлов.
        :rtype: subprocess.Popen
        """

    def _cleanup(self):
        """Удаление временных объектов."""
