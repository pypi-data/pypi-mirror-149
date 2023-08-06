# -*- coding: utf-8 -*-
import base64
import json
from datetime import datetime, date
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5

#
# [ライセンスファイルの構造]
#
# 以下のJSON形式
# ---
#
# {
#  "VERSION": 2,
#  "license_id": <ライセンスID: string>,
#  "hardware_id": <ハードウェアID: string>,
#  "expire_date": <有効期限: string>,
#  "edition": <エディション種別: string>,
#  "licensee": <使用者情報: string>
#  "limits": {
#      "instance": {
#          "Jobflow": <最大ジョブフロー数:non negative integer>,
#          "ScriptJob": <最大スクリプト数:non negative integer>
#      },
#      "node": <最大ノード数:non negative integer>
#  },
#  "signature": <署名文字列: string>,
# }
#
# [注意]
# Kompira Ver.1.4 以降において、ライセンスファイルは前方互換性を確保す
# ること。すなわち、ライセンスファイルのバージョンが新しくなった場合で
# も、以前の Kompira から問題なくインポートできなくてはならない。
#

EXPIRE_DATE_FMT = '%Y-%m-%d'
LICENSE_VERSION = 2


class LicenseError(Exception):
    pass


def _str2date(s):
    if not s:
        return
    if isinstance(s, date):
        return s
    return datetime.strptime(s, EXPIRE_DATE_FMT).date()


def _date2str(d):
    if isinstance(d, date):
        return d.strftime(EXPIRE_DATE_FMT)
    elif isinstance(d, bytes):
        return d.decode()
    return json.JSONEncoder().default(d)


def _to_intdict(d):
    dic = {}
    for key, val in d.items():
        if isinstance(val, dict):
            dic[key] = _to_intdict(val)
        else:
            try:
                dic[key] = int(val)
            except ValueError:
                dic[key] = val
    return dic


class LicenseInfo(object):
    @classmethod
    def loads(cls, lic):
        try:
            dic = json.loads(lic)
            #
            # ライセンスバージョンの確認
            #
            ver = dic.get('VERSION', 1)
            if ver < LICENSE_VERSION:
                raise LicenseError('unsupported version: %s' % ver)
            return cls(**dic)
        except ValueError as e:
            raise LicenseError('invalid format (JSON load error): %s' % e)
        except (AttributeError, TypeError):
            raise LicenseError('invalid format')

    def __init__(self, license_id, hardware_id, expire_date, edition, licensee,
                 limits, signature=None, **kwargs):
        #
        # ライセンス情報のキー値はVER1.5までのライセンスファイルを共通化するため以下の順序にする必要あり
        #
        # ['limits', 'hardware_id', 'licensee', 'signature', 'edition', 'VERSION', 'expire_date', 'license_id']
        #
        #
        self.limits = _to_intdict(limits)
        self.hardware_id = hardware_id
        self.licensee = licensee
        self.signature = signature
        self.edition = edition
        self.VERSION = kwargs.pop('VERSION', LICENSE_VERSION)
        try:
            self.expire_date = _str2date(expire_date)
        except ValueError:
            raise LicenseError('invalid expire date format: %s', expire_date)
        self.license_id = license_id
        self._others = kwargs

    def keys(self):
        keylist = [k for k in self.__dict__.keys() if not k.startswith('_')]
        return keylist + list(self._others.keys())

    def __getitem__(self, key):
        try:
            return self._others[key]
        except KeyError:
            return getattr(self, key)

    def dumps(self, no_signature=True):
        dic = dict(self)
        if no_signature:
            del dic['signature']
        return json.dumps(dic, default=_date2str)

    @property
    def signed(self):
        return self.signature is not None

    def sign(self, prikey):
        private_key = RSA.importKey(prikey)
        h = SHA.new(self.dumps().encode())
        signer = PKCS1_v1_5.new(private_key)
        self.signature = base64.b64encode(signer.sign(h))

    def verify(self, pubkey):
        public_key = RSA.importKey(pubkey)
        h = SHA.new(self.dumps().encode())
        verifier = PKCS1_v1_5.new(public_key)
        signature = base64.b64decode(self.signature)
        return verifier.verify(h, signature)


def gen_rsa_keys(key_length=1024):
    '''Generates Public/Private Key Pair - Returns Public / Private Keys'''
    private = RSA.generate(key_length)
    public = private.publickey()
    private_key = private.exportKey()
    public_key = public.exportKey()

    return private_key.decode(), public_key.decode()
