from io import StringIO
import unittest

from inputs import (InputEqualsValidator, InputIntegerValidator,
                    InputOrValidator, InputInclusiveRangeValidator,
                    InputScanner,)


class TestInputScanner(unittest.TestCase):
    def setUp(self):
        self.default_stop_by = -1
        self.inputs = ['1', '2', '3', str(self.default_stop_by), 'ignored']
        self.expected_size = self.inputs.index(str(self.default_stop_by))
        initial = '\n'.join(self.inputs)
        self.mock_stream = StringIO(initial)
        self.validators_to_fails = [InputEqualsValidator(-2), InputEqualsValidator(-3)]

    def test_input_scanned_values(self):
        '''Tests the values extracted from data stream.'''

        scanner = InputScanner(
            stop_by=self.default_stop_by, data_stream=self.mock_stream
        )

        for i, value in enumerate(scanner):
            expected = int(self.inputs[i])
            self.assertEqual(value, expected)
        with self.assertRaises(StopIteration):
            next(scanner)

    def test_input_scanned_length(self):
        '''Tests if the amount of values extracted from the data stream
        do not pass the `stop_by` defined values.'''

        scanner = InputScanner(
            stop_by=self.default_stop_by, data_stream=self.mock_stream
        )

        scanned_values = list(scanner)
        self.assertEqual(len(scanned_values), self.expected_size)

    def test_invalid_inputs_return_None(self):
        '''Tests if invalid inputs return None as it should to make easy filtering.'''

        scanner = InputScanner(
            stop_by=self.default_stop_by, data_stream=self.mock_stream,
            validators=self.validators_to_fails
        )

        self.assertIs(next(scanner), None)
