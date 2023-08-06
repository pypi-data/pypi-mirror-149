import os
import unittest

import smartparams.utils.string as strutil

_INTEGRATION = strutil.to_bool(os.getenv('TEST_INTEGRATION', default='1'))


@unittest.skipUnless(_INTEGRATION, reason="Integration tests are disabled")
class IntegrationCase(unittest.TestCase):
    pass
