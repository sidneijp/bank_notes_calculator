from io import StringIO
import unittest

from inputs import (InputEqualsValidator, InputIntegerValidator,
                    InputOrValidator, InputInclusiveRangeValidator,
                    InputScanner,)
from main import main


class TestMain(unittest.TestCase):
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
