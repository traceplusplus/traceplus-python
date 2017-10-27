from __future__ import print_function, unicode_literals

import logging
import threading
import opentracing

class Tracer(object):
    """The basic Trace++ client.

    >>> from traceplus import Tracer

    >>> # Read configuration from enviroment ``os.environ['TRACEPLUS_DSN']``
    >>> agent = Tracer()

    >>> # Specify a DSN explicitly
    >>> agent = Tracer(dsn='https://agent_pubkey:agent_secret@traceplus-local.domain/project_id')
    """

    logger = logging.getLogger('traceplus')

    _lock = threading.Lock()
    _initialized = False

    _instance = None

    @staticmethod
    def instance_singleton():
        """
        Ensure the single instance of Tracer
        :return:
        """
        instance = Tracer._instance
        if not instance:
            with Tracer._lock:
                instance = Tracer._instance
                if not instance:
                    instance = Tracer()
                    Tracer._instance = instance
                    Tracer._initialized = True
                    opentracing.tracer = instance

        return instance

    def __init__(self, config = None, **kwargs):
        pass
