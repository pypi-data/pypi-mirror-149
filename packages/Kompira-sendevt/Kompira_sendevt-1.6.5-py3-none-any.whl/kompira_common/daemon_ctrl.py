# -*- coding: utf-8 -*-
import logging
import pwd
import sys
import locale
from daemon import DaemonContext
from kompira_common.version import VERSION


def logging_system_info(logger):
    logger.info("kompira version             = %s", VERSION)
    logger.info("sys.version                 = %s", sys.version)
    logger.info("sys.stdin                   = %s (%s)", sys.stdin, sys.stdin.encoding)
    logger.info("sys.stdout                  = %s (%s)", sys.stdout, sys.stdout.encoding)
    logger.info("sys.stderr                  = %s (%s)", sys.stderr, sys.stderr.encoding)
    logger.info("sys.getdefaultencoding      = %s", sys.getdefaultencoding())
    logger.info("sys.getfilesystemencoding   = %s", sys.getfilesystemencoding())
    logger.info("locale.getdefaultlocale     = %s", ', '.join(locale.getdefaultlocale()))
    logger.info("locale.getpreferredencoding = %s", locale.getpreferredencoding())


class DaemonControl(object):
    """ デーモン制御用クラス """
    def __init__(self, main, name, logger_names=None):
        """
        :param int main: デーモン処理のmain関数
        :param str name: デーモン名
        """
        self._main = main
        self._name = name
        self._logger_names = logger_names or ['kompira']

    def start(self, daemon_mode=False, setuser='', debug_mode=False,
              wdir='/', **options):
        streams = []
        for n in self._logger_names:
            logger = logging.getLogger(n)
            streams += [h.stream for h in logger.handlers]
        if len(streams) > 0:
            stream = streams[0]
        else:
            stream = sys.stderr

        print(f"daemon control: *** started *** '{self._name}'", file=stream)

        uid = None
        gid = None
        if setuser:
            pwnam = pwd.getpwnam(setuser)
            uid = pwnam.pw_uid
            gid = pwnam.pw_gid
            print(f"daemon control: setuser to '{setuser}' (uid={uid}, gid={gid})", file=stream)
        dc = DaemonContext(detach_process=daemon_mode,
                           uid=uid, gid=gid,
                           working_directory=wdir,
                           stdout=stream, stderr=stream,
                           files_preserve=streams)
        with dc:
            self._main(debug_mode, **options)
        print(f"daemon control: *** finished *** '{self._name}'", file=stream)
