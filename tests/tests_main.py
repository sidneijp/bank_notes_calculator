from io import StringIO
import unittest
from unittest.mock import patch

from main import main
import sys

class TestMain(unittest.TestCase):
    def test_a_complete_valid_interaction(self):
        inputs = ['50', '30', '1', '-1', '134', '-1']
        initial = '\n'.join(inputs)
        mock_stream = StringIO(initial)

        main(mock_stream)
