import traceplus

from tests.base import TestCase
from traceplus.conf import Settings

class SettingsTest(TestCase):

    def test_settings_singleton(self):
        s1 = Settings()
        s2 = Settings()

        assert s1 == s2
        assert id(s1) == id(s2)

class InitializeTracerTest(TestCase):

    def test_initialize(self):
        assert callable(traceplus.init_from_module) is True
