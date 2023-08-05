# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

import collections
from ruamel.std.pathlib import Path

__metaclass__ = type

# this should be a class so you can ask .active() on the entry
GrpEntry = collections.namedtuple('GrpEntry', ['gr_' + x for x in [
    'name', 'passwd', 'gid', 'mem']])

# def _is_active(self):
#     if not self.sp_pwd:  # empty password
#         return True
#     return self.sp_pwd[0] not in '*!'
#
# PwdEntry.is_active = _is_active


class Grp:
    def __init__(self, path=None, cache=True):
        self._path = '/etc/group' if path is None else path
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

    def getgrall(self):
        ret_val = []
        for line in self.lines:
            line = line.lstrip()
            if not line or line.startswith('#'):
                continue
            ret_val.append(GrpEntry(*line.split(':')))
        return ret_val

    def getgrnam(self, name):
        name_plus = name + ':'
        for line in self.lines:
            line = line.lstrip()
            if not line or line.startswith('#'):
                continue
            if line.startswith(name_plus):
                return GrpEntry(*line.split(':'))
        raise KeyError("'getgrnam():' name '{}' not found".format(name))

    def getgrgid(self, gid):
        for line in self.lines:
            line = line.lstrip()
            if not line or line.startswith('#'):
                continue
            grp = GrpEntry(*line.split(':'))
            if int(grp.gr_gid) == int(gid):
                return grp
        raise KeyError("'getgrgid():' gid '{}' not found".format(gid))
