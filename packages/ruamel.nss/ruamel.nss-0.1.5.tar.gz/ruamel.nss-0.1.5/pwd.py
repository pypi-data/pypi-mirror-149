# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

import collections
from ruamel.std.pathlib import Path

__metaclass__ = type

# this should be a class so you can ask .active() on the entry
PwdEntry = collections.namedtuple('PwdEntry', ['pw_' + x for x in [
    'name', 'passwd', 'uid', 'gid', 'gecos', 'dir', 'shell']])

# def _is_active(self):
#     if not self.sp_pwd:  # empty password
#         return True
#     return self.sp_pwd[0] not in '*!'
#
# PwdEntry.is_active = _is_active


class Pwd:
    def __init__(self, path=None, cache=True):
        self._path = '/etc/passwd' if path is None else path
        if not hasattr(self._path, 'open'):
            self._path = Path(self._path)
        self._cache = cache  # if True, cache the data
        self._lines = None

    @property
    def lines(self):
        if self._cache:
            if self._lines is not None:
                return self._lines
            self._lines = lines = []
        else:
            lines = []
        for x in self._path.read_text().splitlines():
            lines.append(x.rstrip())
        return lines

    def getpwall(self):
        ret_val = []
        for line in self.lines:
            line = line.lstrip()
            if not line or line.startswith('#'):
                continue
            ret_val.append(PwdEntry(*line.split(':')))
        return ret_val

    def getpwnam(self, name):
        name_plus = name + ':'
        for line in self.lines:
            line = line.lstrip()
            if not line or line.startswith('#'):
                continue
            if line.startswith(name_plus):
                return PwdEntry(*line.split(':'))
        raise KeyError("'getpwnam():' name '{}' not found".format(name))

    def getpwuid(self, uid):
        for line in self.lines:
            line = line.lstrip()
            if not line or line.startswith('#'):
                continue
            pwd = PwdEntry(*line.split(':'))
            if int(pwd.pw_uid) == int(uid):
                return pwd
        raise KeyError("'getpwuid():' uid '{}' not found".format(uid))
