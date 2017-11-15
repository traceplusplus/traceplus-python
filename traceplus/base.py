from __future__ import print_function, unicode_literals

import logging

from traceplus.common.functional import LazyObjectProxy

__all__ = [
    'Tracer',
    'NoopTracer',
    'tracer'
]

class Tracer(object):
    """The basic Trace++ client.
    """
    logger = logging.getLogger('traceplus.tracer')

    def __init__(self, *args, **kwargs):
        pass

    def set_default(self):
        set_default_tracer(self)

class NoopTracer(object):
    def __init__(self, *args, **kwargs):
        pass

    def set_default(self):
        set_default_tracer(self)


default_tracer = None

def get_default_tracer():
    global default_tracer
    return default_tracer

def set_default_tracer(_tracer):
    global default_tracer
    default_tracer = _tracer


tracer = LazyObjectProxy(get_default_tracer)
