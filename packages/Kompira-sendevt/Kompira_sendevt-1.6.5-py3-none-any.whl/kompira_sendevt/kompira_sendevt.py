#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import io
import locale
import amqp
import json
import logging
import optparse
import codecs

from datetime import datetime
from os import pardir, umask
from os.path import abspath, dirname, join
from time import sleep
from uuid import uuid4

sys.path.append(join(dirname(abspath(__file__)), pardir))
from kompira_common.config import Configuration
from kompira_common.qname import IOQ_NAME
from kompira_common.setup_logger import setup_logger, SIMPLE_FORMAT
from kompira_common.version import VERSION

COMMAND_NAME = 'kompira_sendevt'
logger = logging.getLogger('kompira')


class EventConfig(Configuration):
    conf_spec = Configuration.conf_spec
    conf_spec.update(
        {
            # section name
            'event': {
                'channel': (str,
                            '/system/channels/Alert',
                            'channel name for event'),
            },
        })
    # kompira_sendevtはログサイズによるローテーションがデフォルト
    conf_spec['logging'].update(
        {
            'logmaxsz': (
                int, 1024 * 1024 * 1024,
                'log max file size (daily backup if zero)'
            ),
            'logbackup': (int, 10, 'log backup count')
        })


def parse_args():
    usage = "usage: %prog [options] [<key1>=<value1> ...]"
    version = "(Kompira version " + VERSION + ")"
    default_locale, default_encoding = locale.getdefaultlocale()
    default_encoding = default_encoding or 'UTF-8'
    p = optparse.OptionParser(usage, version="%prog " + version)
    p.add_option('-c', '--config', dest='conf', help='Configuration file')
    p.add_option('-s', '--server', dest='server', help='AMQP server')
    p.add_option('-p', '--port', dest='port', help='AMQP port')
    p.add_option('--encoding', dest='encoding', help='Specify encoding of input data', default=default_encoding)
    p.add_option('--decode-stdin', dest='decode_stdin', action='store_true', help='Decode stdin data')
    p.add_option('--user', dest='user', help='User name')
    p.add_option('--password', dest='password', help='User password')
    p.add_option('--ssl', dest='ssl', action='store_true',
                 help='Connect in SSL mode')
    p.add_option('--channel', dest='channel', help='Channel name')
    p.add_option('--site-id', dest='site_id', help='Site ID')
    p.add_option('--max-retry', dest='max_retry',
                 help='max retry count for connection', type='int')
    p.add_option('--retry-interval', dest='retry_interval',
                 help='retry Interval in seconds', type='int')
    p.add_option('--dry-run', dest='dry_run',
                 help='Just check the json data(Do not send alert to Django)',
                 action="store_true", default=False)
    p.add_option('--debug', dest='debug_mode', action='store_true',
                 default=False, help='Starts in debug mode')

    options, args = p.parse_args()
    if not default_locale or not sys.stdout.encoding:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=default_encoding)
    try:
        if len(args) < 1:
            if options.decode_stdin:
                msg = codecs.getreader(options.encoding)(sys.stdin.buffer).read()
            else:
                msg = sys.stdin.buffer.read()
        else:
            msg = dict([arg.split('=', 1) for arg in args if arg])
    except ValueError:
        p.error("invalid message")

    return options, msg


def make_settings(conf, opts):
    # 設定ファイルから読み込む
    settings = {
        'site_id': conf['kompira']['site_id'],
        'channel': conf['event']['channel'],
    }
    settings.update(dict(conf['amqp-connection']))
    settings.update(dict(conf['logging']))

    # コマンドラインオプションで上書き
    for k in settings.keys():
        if hasattr(opts, k) and getattr(opts, k) is not None:
            settings[k] = getattr(opts, k)

    return settings


def send_event(body, settings, dry_run):
    header = {'site_id': settings['site_id'],
              'channel': settings['channel'],
              'timestamp': str(datetime.now())}
    if dry_run:
        event = {
            'settings': settings,
            'application header': header,
        }
        if isinstance(body, dict):
            event['message dict'] = body
        else:
            event['message body'] = stringify(body, True)
        print(stringify(event, encoding=sys.stdout.encoding, indent=2))
        return True

    retry_count = settings['max_retry']
    interval = settings['retry_interval']
    if interval <= 0:
        retry_count = 0
    while True:
        try:
            _send_event(header, body, settings)
            return True
        except amqp.exceptions.AccessRefused as e:
            #
            # Accessエラーの場合、サーバ側の設定の問題のためリトライせずに終了する
            #
            logger.error('failed to send event: %s', e)
            return False
        except Exception as e:
            logger.error('failed to send event: %s', e)
            if retry_count == 0:
                break
            retry_count -= 1
            logger.info('retry connection...')
            sleep(interval)
    return False


def _send_event(header, body, settings):
    with amqp.Connection('%s:%s' % (settings['server'], settings['port']),
                         settings['user'], settings['password'],
                         ssl=settings['ssl']) as conn:
        with conn.channel() as chan:
            chan.queue_declare(queue=IOQ_NAME, durable=True,
                               auto_delete=False,
                               arguments={'x-ha-policy': 'all'})
            corr_id = str(uuid4())
            if isinstance(body, dict):
                msg = amqp.Message(json.dumps(body),
                                   application_headers=header,
                                   content_type='application/json',
                                   correlation_id=corr_id,
                                   delivery_mode=2)
            else:
                msg = amqp.Message(body, application_headers=header,
                                   correlation_id=corr_id,
                                   delivery_mode=2)
            chan.basic_publish(msg, routing_key=IOQ_NAME)
            logger.info('sent message successfully: %s', corr_id)


def stringify(s, quote=False, encoding='utf-8', ensure_ascii=False, indent=None, limit=300):
    if isinstance(s, dict):
        s = json.dumps(s, ensure_ascii=ensure_ascii, indent=indent)
    else:
        msg_len = len(s)
        if msg_len > limit:
            s = s[:limit]
            omit = f'... (length={msg_len})'
        else:
            omit = ''
        if isinstance(s, bytes):
            s = str(s) + omit
        elif isinstance(s, str):
            s = s + omit
        else:
            s = str(s)
    try:
        s.encode(encoding)
    except UnicodeEncodeError as e:
        logger.warning("stringify: %s", e)
        s = s.encode(encoding, errors='backslashreplace').decode(encoding)
    return s


def main():
    try:
        umask(0)  # ログファイルは全ユーザーから書き込み許可で作成される
        opts, msg = parse_args()
        conf = EventConfig(opts.conf)
        settings = make_settings(conf, opts)
        try:
            setup_logger(logger, opts.debug_mode, settings['loglevel'],
                         settings['logdir'], COMMAND_NAME,
                         settings['logmaxsz'], settings['logbackup'], formatter=SIMPLE_FORMAT)
        except IOError as e:
            setup_logger(logger, True, settings['loglevel'],
                         settings['logdir'], COMMAND_NAME, formatter=SIMPLE_FORMAT)
            logger.warning(e)
        logger.info('start: message=%s, options=%s', stringify(msg, True, opts.encoding), opts)
        succeed = send_event(msg, settings, opts.dry_run)
        if not succeed:
            logger.error('gave up retry connection')
            exit(1)
        logger.info('finished')
    except Exception as e:
        logger.exception('failed to send event: %s', e)
        exit(1)


if __name__ == '__main__':
    main()
