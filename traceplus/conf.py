from __future__ import absolute_import, unicode_literals

import logging
import os
import importlib

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from traceplus.common.functional import LazyObjectProxy
from traceplus.utils import exceptions
from traceplus import default_settings
from traceplus import base

__all__ = (
    'settings'
)

ENVIRONMENT_VARIABLE = "TRACEPLUS_SETTINGS_MODULE"

logger = logging.getLogger('traceplus')

class LazySettings(LazyObjectProxy):

    @property
    def configured(self):
        try:
            target = object.__getattribute__(self, '__target__')
        except AttributeError:
            return False
        else:
            return True

    def initialize(self, settings_module, ignore_errors = True):
        if self.configured:
            logger.warning('Settings already configured. Ignore re-init')
            return base.Tracer()

        try:
            self.__wrapped__ = Settings(settings_module)
            return base.Tracer()

        except Exception:
            _raise_configuration_error('settings', None, ignore_errors)
            return base.NoopsTracer()

class BaseSettings(object):
    """
    Common logic for settings whether set by a module or by the user.
    """
    pass

class ErrorTracerSettings(BaseSettings):
    pass

class Settings(BaseSettings):

    _improper_configured = False

    def __init__(self, settings_module = None):
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        if not settings_module:
            self._improper_configured = True
            raise ValueError(
                "Requested settings_module, but settings_module are not configured. "
                "You must either define the environment variable %s "
                "or call `traceplus.init_from_module()`/`traceplus.init_from_file()` "
                "before accessing settings."
                % ENVIRONMENT_VARIABLE)

        for setting in dir(default_settings):
            if setting.isupper():
                setattr(self, setting, getattr(default_settings, setting))

        self.SETTINGS_MODULE = settings_module

        mod = importlib.import_module(self.SETTINGS_MODULE)

        self._user_settings = set()
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)
                self._user_settings.add(setting)

        self._improper_configured = False

def _raise_configuration_error(item, options = None, ignore_errors = True):
    logger.error('CONFIGURATION ERROR!')

    if item:
        logger.error('Item = %s' % item)
    if options:
        logger.error('Options = %r' % options)

    logger.exception('Exception Detail:')
    if not ignore_errors:
        raise exceptions.ImproperlyConfigured(
            'Invalid configuration. Check Traceplus agent '
            'log file for further details.'
        )


settings = LazySettings(Settings)
