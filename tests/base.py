from __future__ import unicode_literals, print_function

VERSION = 1.0

try:
    from unittest2 import TestCase as BaseTestCase
except ImportError:
    from unittest import TestCase as BaseTestCase  # NOQA

class TestCase(BaseTestCase):
    pass
