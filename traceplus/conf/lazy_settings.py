from __future__ import unicode_literals, absolute_import

import sys
import os
import logging

from traceplus.common.functional import LazyObjectProxy
from traceplus.utils import exceptions
from traceplus.conf import default_settings
from traceplus.conf.strategy import strategies
from traceplus import base

ENVIRON_KEY = "TRACEPLUS_SETTINGS"
COMMAND_LINE_ARG = "--traceplus-settings"

logger = logging.getLogger('traceplus')

class LazySettings(LazyObjectProxy):

    @property
    def configured(self):
        try:
            object.__getattribute__(self, '__target__')
        except AttributeError:
            return False
        else:
            return True

    def initialize(self, settings = None, ignore_errors = True):
        """
        Initialize TracerPlus's tracer based on config module.
        If the parameter is None, then use ``os.environ['TRACEPLUS_SETTINGS']``
        initialize the tracer.

        After initialize the tracer, set this instance to opentracing.tracer as
        a global default tracer.

        >>> from traceplus import settings

        >>> # use initialize function to init traceplus
        >>> settings.initialize()
        >>> # Specify a local config module explicitly
        >>> settings.initialize(settings = 'traceplusapp.settings')
        >>> # or specify a local config file
        >>> settings.initialize(settings = 'traceplusapp/settings.py')

        :param settings: the tracer's local configuration module or file
        :param ignore_errors: ignore startup errors
        :return: Tracer instance
        """

        if self.configured:
            logger.warning('Settings already configured. Ignore re-init')
            return base.tracer

        try:
            self.__wrapped__ = Settings(settings)
            tracer = base.Tracer()
        except:
            _raise_configuration_error('settings')
            tracer = base.NoopTracer()

        base.set_default_tracer(tracer)
        return tracer

class Settings(object):

    _improper_configured = False

    def __init__(self, settings_file = None):

        self._settings_file = settings_file

        if self._settings_file is None:
            self._settings_file = self._get_settings_file()

        if not self._settings_file:
            self._improper_configured = True
            raise ValueError(
                "Requested settings_module, but settings_module are not configured. \r\n"
                "Choose one of three strategies below:\r\n"
                "   1. You define the environment variable %s .\r\n"
                "   2. or load your application with `python app.py %s=your_module`.\r\n"
                "   3. or call `traceplus.initialize(module_or_python_file)` before accessing settings.\r\n"
                % (ENVIRON_KEY, COMMAND_LINE_ARG))

        self._load_settings_pipeline()
        self._improper_configured = False

    def _get_settings_file(self):
        return (
            self._get_settings_from_cmd_line() or
            self._get_settings_from_environ()
        )

    def _get_settings_from_cmd_line(self):
        for arg in sys.argv[1:]:
            if arg.startswith(COMMAND_LINE_ARG):
                try:
                    return arg.split('=')[1]
                except IndexError:
                    return
        return

    def _get_settings_from_environ(self):
        if ENVIRON_KEY in os.environ:
            return os.environ[ENVIRON_KEY]
        return

    def _load_settings_pipeline(self):
        strategy = self._get_strategy_by_file(self._settings_file)
        self.SETTINGS_MODULE = strategy.load_settings_file(self._settings_file)

        for setting in dir(default_settings):
            if setting.isupper():
                setattr(self, setting, getattr(default_settings, setting))

        self._user_settings = set()
        for setting in dir(self.SETTINGS_MODULE):
            if setting.isupper():
                setting_value = getattr(self.SETTINGS_MODULE, setting)
                setattr(self, setting, setting_value)
                self._user_settings.add(setting)

    @staticmethod
    def _get_strategy_by_file(settings_file):
        for strategy in strategies:
            if strategy.is_valid_file(settings_file):
                return strategy
        raise RuntimeError('Invalid settings [{}]'.format(settings_file))


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
