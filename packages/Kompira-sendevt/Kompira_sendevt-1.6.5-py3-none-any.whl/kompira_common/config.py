# -*- coding: utf-8 -*-
from configparser import ConfigParser, NoSectionError, NoOptionError


class InvalidSection(Exception):
    pass


class InvalidKey(Exception):
    pass


class Configuration:
    conf_files = ['kompira.conf', '/opt/kompira/kompira.conf']
    conf_spec = {
        # section name
        'kompira': {
            'site_id': (int, 1, 'site id'),
        },
        'logging': {
            'loglevel': (str, 'INFO', 'logging level'),
            'logdir': (str, '/var/log/kompira', 'log directory'),
            'logmaxsz': (int, 0, 'log max file size (daily backup if zero)'),
            'logbackup': (int, 7, 'log backup count'),
        },
        'amqp-connection': {
            # name, type, default-value, description
            'server': (str, 'localhost', 'amqp server name'),
            'port': (int, 5672, 'amqp port'),
            'user': (str, 'guest', 'amqp user name'),
            'password': (str, 'guest', 'amqp user password'),
            'ssl': (bool, False, 'amqp ssl connection'),
            'heartbeat_interval': (
                int, 10, 'amqp heartbeat interval in seconds'
            ),
            'max_retry': (int, 3, 'max retry count for connection'),
            'retry_interval': (int, 30, 'retry interval in seconds'),
        },
        'agent': {
            'name': (str, 'default', 'name of job manager'),
            'pool_size': (int, 8, 'size of worker pool'),
            'disable_cache': (bool, False, 'disable connection cache'),
            'cache_duration': (int, 300, 'duration time (in secs.) of connection cache')
        },
    }

    def __init__(self, conffile=None):
        if conffile is None:
            conffile = self.conf_files
        self._conf = ConfigParser()
        self._conf.read(conffile)
        self._sections = {}

    def __getitem__(self, name):
        if name not in self._sections.keys():
            self._sections[name] = Section(self, name)
        return self._sections[name]

    def _get(self, section, key):
        if section not in self.conf_spec:
            raise InvalidSection(section)
        if key not in self.conf_spec[section]:
            raise InvalidKey(section, key)
        typ, defv, _desc = self.conf_spec[section][key]
        try:
            if typ is bool:
                return self._conf.getboolean(section, key)
            elif typ is int:
                return self._conf.getint(section, key)
            elif typ is float:
                return self._conf.getfloat(section, key)
            else:
                return self._conf.get(section, key)
        except (NoSectionError, NoOptionError):
            return defv


class Section(object):
    def __init__(self, config, name):
        self._config = config
        self._name = name

    def __getitem__(self, key):
        return self._config._get(self._name, key)

    def keys(self):
        return self._config.conf_spec[self._name].keys()
