# -*- coding: utf-8 -*-
import importlib
import sys
import os

class SettingsLoadStrategyPythonModule(object):
    """
    This is the strategy used to read settings from python modules.
    """
    name = 'python_module'

    @staticmethod
    def is_valid_file(file_name):
        try:
            importlib.import_module(file_name)
            return True
        except ImportError:
            return False

    @staticmethod
    def load_settings_file(settings_file):
        return importlib.import_module(settings_file)


LOAD_MODULE_NAME = 'traceplus.user_settings'

class SettingsLoadStrategyPythonFile(object):
    """
    This is the strategy used to read settings from python file.
    """
    name = 'python_file'

    @staticmethod
    def is_valid_file(settings_file):

        if not os.path.exists(settings_file) or not str(settings_file).endswith('py'):
            return False

        return True

    @staticmethod
    def load_settings_file(settings_file):
        if sys.version_info >= (3, 5):
            import importlib.util
            spec = importlib.util.spec_from_file_location(LOAD_MODULE_NAME, settings_file)
            _module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(_module)
            return _module

        elif (3, 3) <= sys.version_info <= (3, 4):
            from importlib.machinery import SourceFileLoader
            return SourceFileLoader(LOAD_MODULE_NAME, settings_file).load_module()

        else:
            import imp
            return imp.load_source(LOAD_MODULE_NAME, settings_file)


strategies = (
    SettingsLoadStrategyPythonModule,
    SettingsLoadStrategyPythonFile
)
