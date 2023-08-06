"""Модуль архиватора виртуальных машин Qemu/KVM."""

import sys
import os
import uuid
import shlex
import signal
import logging
import subprocess
import tempfile
import shutil
import tarfile
from datetime import date
import xml.etree.ElementTree as ET

from msbackup.backend_base import Base as BaseBackend


logger = logging.getLogger('msbackup')


def preexec_fn():  # pragma: no coverage
    """ОТправка сигнала подпроцессу."""
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)


def get_backend_kwargs(params):
    """Подготовка параметров для режима 'kvm'."""
    kwargs = BaseBackend.get_common_backend_kwargs(params)
    BaseBackend.get_param(params, kwargs, 'pool')
    BaseBackend.get_param(params, kwargs, 'filter')
    return kwargs


class Kvm(BaseBackend):
    """
    Архиватор виртуальных машин Qemu/KVM.

    Зависимости:
    - установлены пакеты "KVM":http://www.linux-kvm.org/page/Main_Page и
      "libvirt":http://libvirt.org/index.html;
    - "QEMU Guest agent":http://wiki.libvirt.org/page/Qemu_guest_agent
      установлен на каждой виртуальной машине;
    - образы дисков виртуальных машин в формате
      "qcow2":https://en.wikipedia.org/wiki/Qcow;
    - установлен "pigz":http://zlib.net/pigz;
    - установлен Python3 пакет "libvirt":https://libvirt.org/python.html.
    """

    SECTION = 'Backend-KVM'
    LIBVIRT_CONNECTION = 'qemu:///system'

    @classmethod
    def make_subparser(cls, subparsers):
        """Добавление раздела параметров командной строки для архиватора."""
        parser = subparsers.add_parser('kvm')
        parser.set_defaults(get_backend_kwargs=get_backend_kwargs)
        filter = parser.add_mutually_exclusive_group()
        parser.add_argument(
            '--pool', default='default',
            help='Storage pool name to create snapshot.',
        )
        filter.add_argument(
            '--active', dest='filter', action='store_const', const='active',
            help='Archive only active virtual machines (default).',
        )
        filter.add_argument(
            '--inactive', dest='filter', action='store_const', const='inactive',
            help='Archive only inactive virtual machines.',
        )
        filter.add_argument(
            '--all', dest='filter', action='store_const', const='all',
            help='Archive all virtual machines.',
        )
        parser.add_argument(
            'source', nargs='*', metavar='DOMAIN',
            help='Domain name of virtual machine.')

    def __init__(self, config, *args, **kwargs):
        """Конструктор."""
        super().__init__(config, *args, **kwargs)
        import libvirt
        self.conn = libvirt.open(self.LIBVIRT_CONNECTION)
        self.cwd = None
        self.tmpdir = None
        self.tar_file = None
        self.pool = kwargs.get('pool') or config.get(
            self.SECTION, 'POOL', fallback=None)
        self.filter = kwargs.get('filter') or config.get(
            self.SECTION, 'FILTER', fallback='active')

    def _backup(self, sources=None, **kwargs):
        """
        Архивация виртуальных машин Qemu/KVM.

        :param sources: Список имён виртуальных машин.
        :type sources: [str]
        :return: Количество ошибок.
        :rtype: int
        """
        import libvirt
        if sources is None:
            params = {}
            if self.filter == 'active':
                params['flags'] = libvirt.VIR_CONNECT_LIST_DOMAINS_ACTIVE
            elif self.filter == 'inactive':
                params['flags'] = libvirt.VIR_CONNECT_LIST_DOMAINS_INACTIVE
            domains = self.conn.listAllDomains(**params)
            sources = [dom.name() for dom in domains]
        error_count = 0
        for source in sources:
            output = self.outpath(source)
            logger.info('Backup domain: %s', source)
            try:
                self.archive(
                    source=source,
                    output=output,
                )
            except libvirt.libvirtError as ex:
                error_count += 1
                logger.error('libvirtError: %s', str(ex))
            except subprocess.CalledProcessError as ex:
                logger.error(str(ex))
                error_count += 1
        return error_count

    def _archive(self, source, output=None, **kwargs):
        """
        Упаковка состояния виртуальной машины в архив.

        :param source: Имя домена виртуальной машины.
        :type source: str
        :param output: Путь к файлу архива.
        :type output: str
        :return: Процесс упаковки файлов.
        :rtype: subprocess.Popen
        """
        snapshot = Snapshot(
            conn=self.conn,
            domain_name=source,
            pool=self.pool,
        )
        if snapshot.is_active() and snapshot.has_current_snapshot():
            raise RuntimeError('Domain "%s" has already a snapshot.' % source)
        ext, tar_mode = '.tar', 'w'
        tar_name = source + ext
        self.tmpdir = tempfile.mkdtemp(dir=self.tmp_dir)
        self.cwd = os.getcwd()
        os.chdir(self.tmpdir)
        tar_path = os.path.join(self.tmpdir, tar_name)
        now_str = date.today().isoformat()
        with tarfile.open(tar_path, mode=tar_mode) as tar:
            xml_files = snapshot.dump_xml(path=self.tmpdir)
            for xml_file in xml_files:
                xml_file_name = os.path.basename(xml_file)
                tar.add(
                    name=xml_file,
                    arcname=os.path.join(now_str, xml_file_name)
                )
                logger.debug('file %s added' % xml_file_name)
                os.remove(xml_file)
            snapshot.create_snapshot()
            logger.debug(
                'Adding image files for "%s" to archive "%s"',
                source,
                tar_path,
            )
            try:
                for disk, info in snapshot.disks.items():
                    if info['driver'] != 'qcow2':
                        continue
                    src = info['file']
                    file_name = os.path.basename(src)
                    logger.debug(
                        'Adding "%s" to archive "%s"', file_name, tar_path)
                    tar.add(
                        name=src,
                        arcname=os.path.join(now_str, file_name),
                    )
            except Exception as ex:
                logger.error('ERROR: %s', ex, exc_info=True)
                raise
            finally:
                snapshot.do_blockcommit()
        logger.debug('Compressing "%s"', tar_name)
        if output is None:
            self.tar_file = open(tar_path, mode='rb')
            return self._compress_proc(
                in_stream=self.tar_file,
                out_stream=subprocess.PIPE,
            )
        else:
            with open(tar_path, mode='rb') as tar_file:
                with open(output, mode='wb') as out_file:
                    self._compress(in_stream=tar_file, out_stream=out_file)

    def _cleanup(self):
        """Удаление временных объектов."""
        if self.cwd is not None:
            os.chdir(self.cwd)
            self.cwd = None
        if self.tmpdir is not None:
            shutil.rmtree(self.tmpdir, ignore_errors=True)
            self.tmpdir = None
        if self.tar_file is not None:
            self.tar_file.close()
            self.tar_file = None


class Snapshot():
    """Снимок виртуальной машины."""

    def __init__(self, conn, domain_name, pool=None):
        """Конструктор."""
        self.domain_name = domain_name
        self.snapshot_xml = None
        self.disks = None
        self.snapshot_disk = None
        self.snapshot_id = None
        self.conn = conn
        self.snap_shot = None
        pool_name = pool if pool is not None else 'default'
        self.pool = self.conn.storagePoolLookupByName(pool_name)
        root = ET.fromstring(self.pool.XMLDesc())
        self.pool_path = root.find('./target/path').text

    def get_domain(self):
        """Получение виртуальной машины по имени домена."""
        return self.conn.lookupByName(self.domain_name)

    def is_active(self):
        """Проверка активности виртуальной машины."""
        return self.get_domain().isActive() != 0

    def get_disks(self):
        """Получение всех дисков виртуальной машины."""
        domain = self.get_domain()
        root = ET.fromstring(domain.XMLDesc())
        devices = root.findall('./devices/disk[@device=\'disk\']')
        sources = [device.find('source').attrib for device in devices]
        targets = [device.find('target').attrib for device in devices]
        drivers = [device.find('driver').attrib for device in devices]
        if len(sources) != len(targets):  # pragma: no coverage
            raise RuntimeError(
                'Targets and sources lengths are different %s:%s' %
                (len(sources), len(targets)))
        devs = {}
        for i in range(len(sources)):
            dev = targets[i]['dev']
            devs[dev] = {
                'file': sources[i]['file'],
                'driver': drivers[i]['type'],
            }
        return devs

    def dump_xml(self, path):
        """Сохранение настроек виртуальной машины."""
        import libvirt
        domain = self.get_domain()
        logger.debug('Dumping XMLs for domain %s', domain.name())
        xml_files = []
        dest_file = os.path.join(path, '%s.xml' % domain.name())
        ERROR_MSG = 'File %s already exists!'
        if os.path.exists(dest_file):  # pragma: no coverage
            raise RuntimeError(ERROR_MSG % dest_file)
        with open(dest_file, mode='w') as dest_fh:
            # dump different xmls files. First of all, the offline dump
            xml = domain.XMLDesc()
            dest_fh.write(xml)
        xml_files += [dest_file]
        DEBUG_MSG = 'File %s wrote'
        logger.debug(DEBUG_MSG, dest_file)
        # All flags:
        # - libvirt.VIR_DOMAIN_XML_INACTIVE
        # - libvirt.VIR_DOMAIN_XML_MIGRATABLE
        # - libvirt.VIR_DOMAIN_XML_SECURE
        # - libvirt.VIR_DOMAIN_XML_UPDATE_CPU
        dest_file = '%s-inactive.xml' % domain.name()
        dest_file = os.path.join(path, dest_file)
        if os.path.exists(dest_file):  # pragma: no coverage
            raise RuntimeError(ERROR_MSG % dest_file)
        with open(dest_file, mode='w') as dest_fh:
            # dump different xmls files. First of all, the offline dump.
            xml = domain.XMLDesc(flags=libvirt.VIR_DOMAIN_XML_INACTIVE)
            dest_fh.write(xml)
        xml_files += [dest_file]
        logger.debug(DEBUG_MSG, dest_file)
        # Dump a migrate config file
        dest_file = '%s-migratable.xml' % domain.name()
        dest_file = os.path.join(path, dest_file)
        if os.path.exists(dest_file):  # pragma: no coverage
            raise RuntimeError(ERROR_MSG % dest_file)
        with open(dest_file, mode='w') as dest_fh:
            # dump different xmls files. First of all, the offline dump.
            xml = domain.XMLDesc(
                flags=(libvirt.VIR_DOMAIN_XML_INACTIVE +
                       libvirt.VIR_DOMAIN_XML_MIGRATABLE))
            dest_fh.write(xml)
        xml_files += [dest_file]
        logger.debug(DEBUG_MSG, dest_file)
        return xml_files

    def has_current_snapshot(self):
        """Проверка наличия снимка виртуальной машины."""
        return self.get_domain().hasCurrentSnapshot() != 0

    def get_xml(self):
        """Получение состояния дисков виртуальной машины в формате XML."""
        domain = self.get_domain()
        self.disks = self.get_disks()
        self.snapshot_id = str(uuid.uuid1()).split("-")[0]
        diskspecs = []
        fmt = ('--diskspec %s,'
               'file=%s/snapshot_%s_%s-%s.img')
        for disk in self.disks:
            diskspecs += [fmt % (
                disk, self.pool_path, self.domain_name, disk, self.snapshot_id,
            )]
        my_cmd = (
            'virsh snapshot-create-as --domain {domain_name} '
            '{snapshotId} {diskspecs} --disk-only --atomic --quiesce '
            '--print-xml'.format(
                domain_name=domain.name(),
                snapshotId=self.snapshot_id,
                diskspecs=' '.join(diskspecs),
            )
        )
        logger.debug("Executing: %s", my_cmd)
        create_xml = subprocess.Popen(
            shlex.split(my_cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=preexec_fn,
            shell=False,
        )
        self.snapshot_xml = create_xml.stdout.read().decode('utf-8')
        status = create_xml.wait()
        if status != 0:  # pragma: no coverage
            logger.error('Error for %s:%s', my_cmd, create_xml.stderr.read())
            logger.critical('%s returned %s state', 'virsh', status)
            raise RuntimeError('snapshot-create-as didn\'t work properly')
        return self.snapshot_xml

    def create_snapshot(self):
        """Создание снимка состояния виртуальной машины."""
        import libvirt
        domain = self.get_domain()
        if self.snapshot_xml is None:
            self.get_xml()
        if self.is_active():
            if self.snap_shot is not None:
                logger.error('A snapshot is already defined for this domain')
                logger.warning('Returning the current snapshot')
                return self.snap_shot
            logger.debug(
                'Creating snapshot %s for %s', self.snapshot_id,
                self.domain_name,
            )
            self.snap_shot = domain.snapshotCreateXML(
                self.snapshot_xml,
                flags=sum([
                    libvirt.VIR_DOMAIN_SNAPSHOT_CREATE_DISK_ONLY,
                    libvirt.VIR_DOMAIN_SNAPSHOT_CREATE_ATOMIC,
                    libvirt.VIR_DOMAIN_SNAPSHOT_CREATE_QUIESCE,
                ]),
            )
        else:
            logger.debug('Domain inactive - skip create snapshot')
        self.snapshot_disk = self.get_disks()
        for disk, info in self.snapshot_disk.items():
            top = info['file']
            logger.debug(
                'Created top image %s for %s %s',
                top, domain.name(), disk,
            )
        return self.snap_shot

    def do_blockcommit(self):
        """Выполнение команды blockcommit для каждого диска в снимке."""
        import libvirt
        if not self.is_active():
            logger.debug('Domain inactive - skip blockcommit')
            return
        if self.snap_shot is None:
            raise RuntimeError('no snapshot of domain')
        encoding = sys.getdefaultencoding()
        domain = self.get_domain()
        logger.debug("Blockcommitting %s", domain.name())
        for disk in self.disks:
            my_cmd = (
                'virsh blockcommit {domain_name} {disk} --pivot'
            ).format(domain_name=domain.name(), disk=disk)
            logger.debug('Executing: %s', my_cmd)
            blockcommit = subprocess.Popen(
                shlex.split(my_cmd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=preexec_fn,
                shell=False,
            )
            for line in blockcommit.stdout:
                line = line.strip()
                if len(line) > 0:
                    logger.debug(line.decode(encoding))
            status = blockcommit.wait()
            if status != 0:
                logger.error(
                    'Error for %s => %s', my_cmd, blockcommit.stderr.read())
                logger.critical('%s returned %s state', 'virsh', status)
                raise RuntimeError('blockcommit didn\'t work properly')
        test_disks = self.get_disks()
        for disk, base_info in self.disks.items():
            base = base_info['file']
            test_base = test_disks[disk]['file']
            top = self.snapshot_disk[disk]['file']
            if base == test_base and top != test_base:
                logger.debug('Removing %s', top)
                self.pool.refresh()
                vol = self.pool.storageVolLookupByName(os.path.basename(top))
                vol.delete()
            else:  # pragma: no coverage
                logger.error('original base: %s, top: %s, new_base: %s',
                             base, top, test_base)
                raise RuntimeError(
                    'Something goes wrong for snaphost %s', self.snapshot_id)
        logger.debug('Removing snapshot %s', self.snapshot_id)
        metadata = [libvirt.VIR_DOMAIN_SNAPSHOT_DELETE_METADATA_ONLY]
        self.snap_shot.delete(flags=sum(metadata))
