# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

_package_data = dict(
    full_package_name='ruamel.nss',
    version_info=(0, 1, 5),
    __version__='0.1.5',
    version_timestamp='2022-03-16 14:33:40',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='managing passwd, group and shadow under /etc, /usr/lib/extrausers, etc.',
    # keywords="",
    # entry_points='nss=ruamel.nss.__main__:main',
    entry_points=None,
    license='Copyright Ruamel bvba 2007-2016',
    since=2016,
    # status: "α|β|stable",  # the package status on PyPI
    # data_files="",
    # universal=True,
    install_requires=['ruamel.std.pathlib'],
        # py27=["ruamel.ordereddict"],
     python_requires='>=3',

)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']
