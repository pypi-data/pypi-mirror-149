# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

"""
re-implemenation of the spwd (which is hard-coded to use /etc/shadow), to also allow
reading of libnss managed files.

chroot-ing doesn't really work as this still requires the files to be under /etc
"""

import collections
from ruamel.std.pathlib import Path

__metaclass__ = type


# this should be a class so you can ask .active() on the entry
SpwdEntry = collections.namedtuple('SpwdEntry', ['sp_' + x for x in [
    'namp', 'pwdp', 'lstchg', 'min', 'max', 'warn', 'inact', 'expire', 'flag']])


def _is_active(self):
    if not self.sp_pwdp:  # empty password
        return True
    return self.sp_pwdp[0] not in '*!'

SpwdEntry.is_active = _is_active


class Spwd:
    def __init__(self, path=None, cache=True):
        self._path = '/etc/shadow' if path is None else path
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

    def getspall(self):
        ret_val = []
        for line in self.lines:
            line = line.lstrip()
            if not line or line.startswith('#'):
                continue
            ret_val.append(SpwdEntry(*line.split(':')))
        return ret_val

    def getspnam(self, name):
        name_plus = name + ':'
        for line in self.lines:
            line = line.lstrip()
            if not line or line.startswith('#'):
                continue
            if line.startswith(name_plus):
                return SpwdEntry(*line.split(':'))
        raise KeyError("'getspnam():' name '{}' not found".format(name))

    def active_users(self):
        for x in self.getspall():
            if x.is_active:
                yield x[0]


if __name__ == '__main__':
    spwd = Spwd('/data1/DOCKER/extrausers/shadow')
    x = spwd.getspall()
    print(x[1])
    print(x[1].sp_nam, x[1].sp_pwd)
    for x in spwd.active_users():
        print(x)
