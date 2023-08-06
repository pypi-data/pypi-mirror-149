# -*- coding: utf-8 -*-
import logging
import socket
import errno
from time import sleep

import amqp
from amqp.exceptions import UnexpectedFrame

logger = logging.getLogger('kompira')


_parameters = {
    'host': 'localhost:5672',
    'userid': 'guest',
    'password': 'guest',
    'ssl': False
}


def amqp_setup(host, user, password, ssl, heartbeat=None, **kwargs):
    _parameters['host'] = host
    _parameters['userid'] = user
    _parameters['password'] = password
    _parameters['ssl'] = ssl
    _parameters['heartbeat'] = heartbeat
    _parameters.update(**kwargs)


class AMQPConnectorMixin(object):
    def _connect(self):
        self._consumers = []
        self._conn = amqp.Connection(on_blocked=self._on_blocked, on_unblocked=self._on_unblocked, **_parameters)
        self._conn.connect()
        self._chan = self._conn.channel()
        logger.info('[%s] established connection to AMQP', self.__class__.__name__)

    def _on_blocked(self, reason):
        logger.warning('[%s] amqp connection blocked: %s', self.__class__.__name__, reason)

    def _on_unblocked(self):
        logger.info('[%s] amqp connection unblocked', self.__class__.__name__)

    def _close(self):
        #
        # 登録済みハンドラの削除
        #
        for ctag in self._consumers:
            try:
                self._chan.basic_cancel(ctag)
            except (IOError, AttributeError) as e:
                # RabbitMQ 切断時に amqp の basic_cancel() で AttributeError
                # が起きることがある
                logger.warning('[%s] failed to unregister handler: [ctag=%s] %s', self.__class__.__name__, e, ctag)
        del self._consumers[:]
        #
        # コネクションのクローズ
        #
        try:
            if self._chan:
                self._chan.close()
            if self._conn:
                self._conn.close()
        except IOError as e:
            logger.error('[%s] failed to close connection: %s', self.__class__.__name__, e)

    def _register_handler(self, qname, handler, **kwargs):
        ctag = self._chan.basic_consume(queue=qname, callback=handler, **kwargs)
        self._consumers.append(ctag)
        return ctag

    def _retry_loop(self, max_retry=-1, retry_interval=10):
        retry_count = max_retry
        while True:
            try:
                self._connect()
                #
                # 接続確立したらretry_countをリセットしておく
                #
                retry_count = max_retry
                self._loop()
                break
            except socket.error as e:
                logger.error('[%s] socket error: %s', self.__class__.__name__, e)
            except amqp.ConnectionError as e:
                logger.error('[%s] AMQP connection error: %s', self.__class__.__name__, e)
            except KeyboardInterrupt:
                logger.info('[%s] keyboard interrupted', self.__class__.__name__)
                break
            except Exception as e:
                logger.exception('[%s] %s', self.__class__.__name__, e)
                break
            finally:
                self._close()
            #
            # 再接続処理
            #
            if retry_count == 0:
                logger.error('[%s] gave up retry connection', self.__class__.__name__)
                break
            elif max_retry > 0:
                retry_count -= 1
            logger.info('[%s] waiting %s seconds for retry connection ...', self.__class__.__name__, retry_interval)
            self._wait(retry_interval)
            logger.info('[%s] retry connection', self.__class__.__name__)

    def _wait(self, retry_interval):
        sleep(retry_interval)

    def _drain_events(self, timeout=0):
        #
        # timeout=0指定時、socketはノンブロッキングモード
        #
        try:
            while True:
                self._conn.drain_events(timeout=timeout)
        except socket.timeout:
            if timeout != 0:
                raise
            return
        except socket.error as e:
            if e.errno != errno.EAGAIN:
                raise
        #
        # 不正なフレームを受信するとAMQPが例外を投げるため
        # キャッチしておく
        #
        except (UnicodeDecodeError, AttributeError, UnexpectedFrame) as e:
            logger.exception('[%s] %s: %s', type(self).__name__, e.__class__.__name__, e)

