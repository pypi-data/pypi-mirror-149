import os
import unittest

import smartparams.utils.string as strutil

_UNIT = strutil.to_bool(os.getenv('TEST_UNIT', default='1'))


@unittest.skipUnless(_UNIT, reason="Unit tests are disabled")
class UnitCase(unittest.TestCase):
    pass
