# -*- coding: utf-8 -*-
import os
import sys
import logging
import multiprocessing
from queue import Empty
from threading import Thread, current_thread
from datetime import datetime



def _now():
    n = datetime.now()
    return n.strftime("%Y-%m-%d %H:%M:%S") + ",{:03}".format(int(n.microsecond / 1000))


def _logging(level, msg, *args):
    message = msg % args
    procname = multiprocessing.current_process().name
    threadid = current_thread().ident
    threadname = current_thread().name
    print(f"[{_now()}:{os.getpid()}:{procname}:{threadid}:{threadname}] {level}: [MPLog] {message}")
    sys.stdout.flush()


def _error(msg, *args):
    _logging('ERROR', msg, *args)


def _warn(msg, *args):
    _logging('WARN', msg, *args)


def _debug(msg, *args):
    _logging('DEBUG', msg, *args)


class MPLogger(logging.Logger):
    #
    # https://gist.github.com/schlamar/7003737
    #
    _is_active = False
    _log_queue = None
    _log_thread = None
    _log_pid = None

    def isEnabledFor(self, level):
        return True

    def handle(self, record):
        ei = record.exc_info
        if ei:
            # to get traceback text into record.exc_text
            logging._defaultFormatter.format(record)
            record.exc_info = None  # not needed any more
        d = dict(record.__dict__)
        d['msg'] = record.getMessage()
        d['args'] = None
        self._log_queue.put_nowait(d)

    @classmethod
    def _daemon(cls, _log_queue):
        current_thread().name = "MPLogger"
        try:
            _debug("mplog.daemon: logger daemon started: fno=%s", [_log_queue._reader.fileno(), _log_queue._writer.fileno()])
            while True:
                try:
                    record_data = _log_queue.get(timeout=1)
                    if record_data is None:
                        _debug("mplog.daemon: receive stop signal")
                        break
                    record = logging.makeLogRecord(record_data)
                    logger = logging.getLogger(record.name)
                    if logger.isEnabledFor(record.levelno):
                        logger.handle(record)
                except Empty:
                    if not cls._is_active:
                        _debug("mplog.daemon: detect stop signal")
                        break
                except (KeyboardInterrupt, SystemExit, IOError):
                    raise
                except EOFError:
                    break
                except:
                    logging.exception('Error in log handler.')
        finally:
            _debug("mplog.daemon: logger daemon finished")

    @classmethod
    def start(cls):
        assert cls._log_pid is None
        assert cls._log_thread is None
        cls._is_active = True
        cls._log_pid = os.getpid()
        cls._log_queue = multiprocessing.Queue()
        cls._log_queue.cancel_join_thread()
        cls._log_thread = Thread(target=cls._daemon, args=(cls._log_queue,))
        cls._log_thread.daemon = True
        cls._log_thread.start()

    @classmethod
    def terminate(cls):
        _debug("mplog.terminate: stop logger daemon thread")
        assert cls._log_pid == os.getpid()
        assert cls._log_thread is not None
        cls._log_queue.put_nowait(None)
        cls._is_active = False
        cls._log_thread.join(5.0)
        cls._log_thread = None
        cls._log_queue = None
        cls._log_pid = None
        _debug("mplog.terminate: finished")

    @classmethod
    def logged_call(cls, func, *args, **kwargs):
        logging._acquireLock()
        try:
            if cls._log_pid is not None and cls._log_pid != os.getpid():
                logging.setLoggerClass(cls)
                # monkey patch root logger and already defined loggers
                # _debug("mplog.logged_call: replace root-logger %s to MPLogger", logging.root)
                logging.root.__class__ = cls
                for key, logger in logging.Logger.manager.loggerDict.items():
                    #_debug("mplog.logged_call: loggerDict[%s] = %s", key, logger)
                    #if not isinstance(logger, logging.PlaceHolder):
                    #    logger.__class__ = cls
                    if isinstance(logger, logging.Logger):
                        # _debug("mplog.logged_call: replace loggerDict[%s] %s to MPLogger", key, logger)
                        logger.__class__ = cls
            else:
                _warn("mplog.logged_call: direct logging")
            for key, logger in logging.Logger.manager.loggerDict.items():
                if not isinstance(logger, logging.Logger):
                    continue
                for handler in logger.handlers:
                    lock = handler.lock
                    if not lock:
                        continue
                    if lock.acquire(False):
                        lock.release()
                    else:
                        _error("mplog.logged_call: %s of logger '%s' %s is locked", handler, logger.name, logger)
        finally:
            logging._releaseLock()

        func(*args, **kwargs)
