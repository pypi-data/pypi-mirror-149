#!/usr/bin/env python
"""
msbackup -- Generic archive utility.

@author:     Aleksei Badiaev <aleksei.badyaev@gmail.com>
@copyright:  2015 Aleksei Badiaev. All rights reserved.
"""

import os
import sys
import traceback
import argparse
import configparser
import logging

import msbackup
from msbackup import flock
from msbackup import backend
from msbackup.backend_base import Base as BaseBackend


__all__ = ('main', )
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DEBUG = False
logger = logging.getLogger('msbackup')


def main(argv=None):
    """
    Точка входа в приложение.

    :param argv: Аргументы командной строки.
    :type argv: list
    :return: Код завершения приложения.
    :rtype: int
    """
    global DEBUG
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = 'v%s' % msbackup.__version__
    program_build_date = str(msbackup.__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (
        program_version, program_build_date,
    )
    program_shortdesc = __import__('msbackup').cli.__doc__.split('\n')[1]
    program_license = """%s

  Created by Aleksei Badiaev <aleksei.badyaev@gmail.com> on %s.
  Copyright 2015 Aleksei Badiaev. All rights reserved.

  Distributed on an 'AS IS' basis without warranties
  or conditions of any kind, either express or implied.
""" % (program_shortdesc, str(msbackup.__date__))

    class LogFilter(object):
        """Фильтр сообщений журнала."""

        def __init__(self, max_level=logging.ERROR):
            """Конструктор."""
            self.max_level = max_level

        def filter(self, record):
            """Фильтрация сообщений."""
            return record.levelno < self.max_level

    # Configure logging.
    log_error_handler = logging.StreamHandler(sys.stderr)
    log_error_handler.setLevel(logging.ERROR)
    logger.addHandler(log_error_handler)
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.addFilter(LogFilter())
    log_handler.setLevel(logging.NOTSET)
    logger.addHandler(log_handler)
    logger.setLevel(logging.ERROR)

    try:
        parser = argparse.ArgumentParser(
            prog=program_name,
            description=program_license,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        subparsers = BaseBackend.make_options(parser=parser)
        parser.add_argument(
            '-l', '--lock', action='store_true',
            help='Allow only one instance of the application to run.',
        )
        parser.add_argument(
            '-d', '--debug', action='store_true',
            help='Print traceback when errors occured.',
        )
        parser.add_argument(
            '-v', '--verbose', action='count', default=0,
            help='Verbose output.',
        )
        parser.add_argument(
            '-V', '--version', action='version',
            version=program_version_message,
        )
        for backend_name in backend.INIT_BACKENDS_LIST:
            backend.BACKENDS[backend_name].make_subparser(subparsers)
        params = parser.parse_args()
        DEBUG = params.debug
        verbose = params.verbose
        if verbose > 1:
            log_handler.setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)
        elif verbose > 0:
            log_handler.setLevel(logging.INFO)
            logger.setLevel(logging.INFO)
        if params.lock:
            lockfile_path = os.path.join(
                "/tmp",
                os.path.splitext(os.path.basename(sys.argv[0]))[0] + ".lock",
            )
            lock = flock.Flock(lockfile_path, debug=DEBUG).acquire()
            if not lock:  # pragma: no coverage
                raise RuntimeError(
                    'Another istance of "%s" is running. '
                    'Please wait for its termination or kill the running '
                    'application.' % sys.argv[0])
        config = configparser.RawConfigParser()
        if params.config is not None:
            config_file_path = params.config
            if not os.path.isfile(config_file_path):
                raise FileNotFoundError(config_file_path)
            config.read(config_file_path)
            setattr(config, 'config_file_path', config_file_path)
        BaseBackend.validate_params(parser, params)
        # Perform backup.
        return backend.make_backend(
            name=params.backend,
            config=config,
            **params.get_backend_kwargs(params),
        ).backup(sources=getattr(params, 'source', None))
    except KeyboardInterrupt:  # pragma: no coverage
        return 0
    except Exception as ex:
        logger.error('%s: %s', type(ex).__name__, str(ex))
        if DEBUG:  # pragma: no coverage
            traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no coverage
    sys.exit(main())
