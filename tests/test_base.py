import os
import importlib

import traceplus
from traceplus.conf import Settings, ENVIRON_KEY
from traceplus.base import Tracer, NoopTracer

from tests.base import TestCase

class SettingsTest(TestCase):
    def test_settings(self):
        s = Settings('traceplus.conf.default_settings')
        self.assertIsNotNone(s)

class InitializeTracerTest(TestCase):
    def setUp(self):
        self.clear_traceplus()

    def tearDown(self):
        self.clear_traceplus()

    def clear_traceplus(self):
        try:
            del traceplus.settings.__wrapped__
        except AttributeError:
            pass

        try:
            del traceplus.tracer.__wrapped__
        except AttributeError:
            pass

    def test_init_callable(self):
        assert callable(traceplus.initialize) is True

    def test_init_from_module(self):
        traceplus.initialize('traceplus.conf.default_settings', ignore_errors = True)

        self.assertIsNotNone(traceplus.tracer)
        self.assertIsNotNone(traceplus.base.tracer)
        self.assertTrue(traceplus.tracer == traceplus.base.tracer)
        self.assertIs(traceplus.tracer, traceplus.base.tracer)

        self.assertIsInstance(traceplus.base.tracer, Tracer)
        self.assertIsInstance(traceplus.tracer, Tracer)

    def test_init_from_file(self):
        root_dir = os.path.dirname(traceplus.__file__)
        traceplus.initialize(
            os.path.join(root_dir, 'conf', 'default_settings.py'), ignore_errors = True)

        self.assertIsNotNone(traceplus.tracer)
        self.assertIsNotNone(traceplus.base.tracer)
        self.assertTrue(traceplus.tracer == traceplus.base.tracer)
        self.assertIs(traceplus.tracer, traceplus.base.tracer)

        self.assertIsInstance(traceplus.base.tracer, Tracer)
        self.assertIsInstance(traceplus.tracer, Tracer)

    def test_missed_module(self):
        traceplus.initialize()

        self.assertIsNotNone(traceplus.tracer)
        self.assertIsNotNone(traceplus.base.tracer)
        self.assertTrue(traceplus.tracer == traceplus.base.tracer)
        self.assertIs(traceplus.tracer, traceplus.base.tracer)

        self.assertIsInstance(traceplus.base.tracer, NoopTracer)
        self.assertIsInstance(traceplus.tracer, NoopTracer)
