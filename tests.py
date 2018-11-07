from io import StringIO
import unittest
from unittest.mock import patch

from main import main, InputScanner


class TestMain(unittest.TestCase):
    def test_it_runs(self):
        self.assertTrue(main())

    def test_parse_user_inputs(self):
        inputs = ['50', '30', '-1', '2']
        initial = '\n'.join(inputs)
        mock_stream = StringIO(initial)

        scanner = InputScanner(stop_by=-1, data_stream=mock_stream)

        for i, value in enumerate(scanner):
            expected = int(inputs[i])
            self.assertEqual(value, expected)
        with self.assertRaises(StopIteration):
            next(scanner)
