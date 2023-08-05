
the standard library ``pwd``, ``grp`` and ``spwd`` are hard wired
to use ``/etc/passwd``, ``/etc/group`` and ``/etc/shadow`` respectively.

That makes them useless for managing these files when they reside somewhere else,
which is e.g. the case when using ``libnss``.

This library reimplements the functionality by creating three classes that default
to opening the files under `/etc`, but which can be given explicit paths.

The original module level routines are now methods on the instances that return named tuples
with the fieldnames being the same as those from the stdlib modules.

This library uses the new (corrected) names for the fields. In particular ``sp_namep`` and
``sp_pwdp`` as used in Python 3 instead of the versions without trailing ``p`` from 2.7
