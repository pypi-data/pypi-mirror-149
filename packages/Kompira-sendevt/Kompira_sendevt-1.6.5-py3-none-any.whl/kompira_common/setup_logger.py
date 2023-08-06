# -*- coding: utf-8 -*-
import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from os.path import join

SIMPLE_FORMAT = '[%(asctime)s:%(process)d:%(processName)s] %(levelname)s: %(message)s'
DEFAULT_FORMAT = '[%(asctime)s:%(process)d:%(processName)s:%(threadName)s] %(levelname)s: %(message)s'
VERBOSE_FORMAT = '[%(asctime)s:%(process)d:%(processName)s:%(thread)d:%(threadName)s] %(levelname)s: %(message)s'

PROCESS_DEFAULT_FORMAT = '[%(asctime)s:%(process)d:%(processName)s:%(threadName)s] Process(%(proc_id)s): %(message)s'
PROCESS_DEBUG_FORMAT = '[%(asctime)s:%(process)d:%(processName)s:%(thread)d:%(threadName)s] Process(%(proc_id)s): %(message)s'


def setup_logger(logger, debug_mode,
                 loglevel='INFO', logdir='./', logname='kompira',
                 maxsz=0, backup=7, when='D',
                 formatter=None):
    lvl = getattr(logging, loglevel)
    fnm = join(logdir, logname + '.log')
    if debug_mode:
        hdl = logging.StreamHandler()
        lvl = logging.DEBUG
    elif maxsz > 0:
        hdl = RotatingFileHandler(filename=fnm, maxBytes=maxsz,
                                  backupCount=backup)
    else:
        hdl = TimedRotatingFileHandler(filename=fnm, when=when,
                                       backupCount=backup)
    if any(isinstance(h, hdl.__class__) for h in logger.handlers):
        #
        # 同クラスのハンドラを二重登録しない
        #
        logger.warn("setup_logger('%s', %s, %s): %s has registered already", logger.name, debug_mode, loglevel, hdl.__class__.__name__)
    else:
        if not formatter:
            formatter = VERBOSE_FORMAT if debug_mode else DEFAULT_FORMAT
        fmt = logging.Formatter(formatter)
        hdl.setFormatter(fmt)
        hdl.setLevel(lvl)
        logger.addHandler(hdl)
    logger.setLevel(lvl)
