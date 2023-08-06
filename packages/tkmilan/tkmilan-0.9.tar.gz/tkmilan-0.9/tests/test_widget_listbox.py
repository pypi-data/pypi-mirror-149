# import typing
import unittest
import logging

# import tkmilan.util

logger = logging.getLogger(__name__)


class Test_Listbox_Order(unittest.TestCase):
    pass


if __name__ == '__main__':
    import sys
    logs_lvl = logging.DEBUG if '-v' in sys.argv else logging.INFO
    logging.basicConfig(level=logs_lvl, format='%(levelname)5.5s:%(funcName)s: %(message)s', stream=sys.stderr)
    unittest.main()
