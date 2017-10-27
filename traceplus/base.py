from __future__ import print_function, unicode_literals

import logging
import opentracing

from traceplus.utils.pattern import Singleton
from traceplus.packages import six

class Tracer(six.with_metaclass(Singleton, object)):
    """The basic Trace++ client.
    """

    logger = logging.getLogger('traceplus.tracer')

    def __init__(self, **kwargs):
        pass


class NoopsTracer(Tracer):
    pass
