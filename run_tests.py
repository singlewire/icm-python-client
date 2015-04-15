import unittest
from tests.unit.test_icm_client import TestICMClient

suite = unittest.TestLoader().loadTestsFromTestCase(TestICMClient)
unittest.TextTestRunner(verbosity=2).run(suite)