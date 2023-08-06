#!/usr/bin/env python3
# coding: utf-8

import os

import volkanic.environ
from volkanic.utils import (
    under_home_dir, abs_path_join, abs_path_join_and_mkdirs
)


class GlobalInterface(volkanic.environ.GlobalInterfaceTrial):
    package_name = 'm14.meta'

    def under_data_dir(self, *paths, mkdirs=False):
        if 'data_dir' not in self.conf:
            names = self.package_name.split('.')
            data_dir = os.path.join('/data/local', *names)
            self.conf.setdefault('data_dir', data_dir)
        return super().under_data_dir(*paths, mkdirs=mkdirs)

    @classmethod
    def under_m14_dir(cls, *paths, mkdirs=False):
        base_dir = os.environ.get('JOKER_HOME') or under_home_dir('.m14')
        if not mkdirs:
            return abs_path_join(base_dir, *paths)
        return abs_path_join_and_mkdirs(base_dir, *paths)

    @classmethod
    def under_m14_subdir(cls, *paths, mkdirs=False):
        _paths = cls.namespaces[1:]
        _paths.extend(paths)
        return cls.under_m14_dir(*_paths, mkdirs=mkdirs)

    @classmethod
    def _get_conf_path_names(cls):
        names = cls.namespaces.copy()
        names.append(cls._get_option('confpath_filename'))
        return names
