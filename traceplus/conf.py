from __future__ import absolute_import, unicode_literals

import logging
import os
import six

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from traceplus.utils.pattern import Factory, Singleton
from traceplus.utils.exceptions import ImproperlyConfigured

logger = logging.getLogger('traceplus')

def _initialize_tracer(config = None, ignore_errors = True):
    """
    Initialize TracerPlus's tracer based on config file.
    If the parameter is None, then use ``os.environ['TRACE_PLUS_CONFIG']``
    initialize the tracer. The local config file allways has higher priority.

    After initialize the tracer, set this instance to opentracing.tracer as
    a global default tracer.

    >>> from traceplus import initialize

    >>> # Read configuration from enviroment ``os.environ['TRACE_PLUS_CONFIG']``
    >>> agent = initialize()

    >>> # Or specify a local config file explicitly
    >>> agent = initialize(config = '/etc/traceplus/traceplus.yaml')

    :param config: the tracer's local configuration file path.
    :param ignore_errors: ignore startup errors
    :return: Tracer instance
    """

    try:
        return SettingsFactory().create(config, ignore_errors = ignore_errors).initialize_tracer()
    except:
        pass

class Settings(object):
    """
    Common logic for settings whether set by a module or by the user.
    """
    pass

class ErrorTracerSettings(Settings):
    pass

class TracePlusSettings(six.with_metaclass(Singleton, Settings)):

    # application name
    app_name = os.environ.get('TRACE_PLUS_APP_NAME', 'Python Application')

    # tracer is enabled or not
    enabled = _environ_as_bool('TRACE_PLUS_ENABLED', True)

    # the default log_file path
    log_file = os.environ.get('TRACE_PLUS_LOG', '/tmp/traceplus_agent.log')

    # application public/secret key
    public_key = os.environ.get('TRACE_PLUS_PUBLIC_KEY', None)
    secret_key = os.environ.get('TRACE_PLUS_SECRET_KEY', None)

    error_tracer = ErrorTracerSettings()

    def __init__(self, config, ignore_errors):
        pass

    def initialize_tracer(self):
        pass

class SettingsFactory(Factory):

    def create(self, config = None, **kwargs):
        ignore_errors = kwargs.get('ignore_errors', True)

        # use config as first choice
        if config is None:
            config = os.environ.get('TRACE_PLUS_CONFIG', None)

        if config:
            return TracePlusSettings(config, ignore_errors)

def _raise_configuration_error(section, item):

    logger.error('CONFIGURATION ERROR')

    if section:
        pass


def _environ_as_bool(name, default=False):
    flag = os.environ.get(name, default)
    if default is None or default:
        try:
            flag = not flag.lower() in ['off', 'false', '0']
        except AttributeError:
            pass
    else:
        try:
            flag = flag.lower() in ['on', 'true', '1']
        except AttributeError:
            pass
    return flag
