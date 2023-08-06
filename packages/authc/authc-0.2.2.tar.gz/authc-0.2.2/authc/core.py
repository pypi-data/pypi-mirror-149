import json
import platform
import subprocess
import sys
import threading
import time
from typing import Dict

import codefast as cf
from codefast.patterns.singleton import SingletonMeta
import os


class Authentication(object):
    @classmethod
    def exec(cls):
        d = os.path.join(os.environ['HOME'], '.config/textauth')
        if not cf.io.exists(d):
            cf.error('textauth not exists')
            return ""
        master = 'bDVlQnR2ZTdtM1MzcjZnVAo'
        cmd = f'openssl bf -iter 1024 -d -k {master} < {d}'
        return cf.shell(cmd)


def authc() -> Dict[str, str]:
    try:
        texts = Authentication.exec()
        dt = {}
        for ln in texts.split('\n'):
            if ln:
                k, v = ln.split(':', 1)
                dt[k] = v
        return dt
    except Exception as e:
        cf.error(e)
        return {}


def gunload(key: str) -> str:
    return authc().get(key, '')
