import traceplus

from .base import TestCase
from traceplus.conf import TracePlusSettings

class SettingsTest(TestCase):

    def test_settings_singleton(self):
        s1 = TracePlusSettings('/etc/traceplus/traceplus.yaml', False)
        s2 = TracePlusSettings('/etc/traceplus/traceplus.yaml', False)

        assert s1 == s2
        assert id(s1) == id(s2)

class InitializeTracerTest(TestCase):

    def test_initializer_tracer(self):
        assert callable(traceplus.initialize) is True
