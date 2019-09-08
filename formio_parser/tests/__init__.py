# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import sys

# Workaround `ValueError: attempted relative import beyond top-level package`
sys.path.append('..')

from . import test_common
from . import test_builder
from . import test_submission
