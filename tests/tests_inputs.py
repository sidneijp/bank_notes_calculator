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


class TestInputEqualsValidator(unittest.TestCase):
    def setUp(self):
        self.values = [-1, 0, 10000, 999]
        self.expected_values = zip(self.values, self.values)
        self.unexpected_values = zip(self.values, [-2, 1, -100, 99])

    def test_expected_values(self):
        for v, e in self.expected_values:
            validator = InputEqualsValidator(v)
            self.assertTrue(validator.validate(e))

    def test_unexpected_values(self):
        for v, u in self.unexpected_values:
            validator = InputEqualsValidator(v)
            self.assertFalse(validator.validate(u))


class TestInputInclusiveRangeValidator(unittest.TestCase):
    def setUp(self):
        self.lower = 10
        self.upper = 100
        self.validator = InputInclusiveRangeValidator(self.lower, self.upper)

    def test_value_inside_range(self):
        value = (self.lower + self.upper) / 2
        self.assertTrue(self.validator.validate(value))

    def test_value_in_range_limits(self):
        value = self.lower
        self.assertTrue(self.validator.validate(value))
        value = self.upper
        self.assertTrue(self.validator.validate(value))

    def test_value_out_of_range(self):
        value = self.lower - 1
        self.assertFalse(self.validator.validate(value))
        value = self.upper + 1
        self.assertFalse(self.validator.validate(value))


class TestInputIntegerValidator(unittest.TestCase):
    def setUp(self):
        self.validator = InputIntegerValidator()

    def test_is_integer(self):
        self.assertIsInstance(0, int)

    def test_is_not_integer(self):
        self.assertFalse(isinstance('a', int))
        self.assertFalse(isinstance(1.0, int))
        self.assertFalse(isinstance([], int))
        self.assertFalse(isinstance(tuple(), int))
        self.assertFalse(isinstance({}, int))


class TestInputOrValidator(unittest.TestCase):
    def test_all_validators_true(self):
        validator = InputOrValidator([
            InputIntegerValidator(),
            InputEqualsValidator(0),
            InputInclusiveRangeValidator(0, 10),
        ])
        value = 0
        self.assertTrue(validator.validate(value))

    def test_none_validators_false(self):
        validator = InputOrValidator([
            InputEqualsValidator(0),
            InputInclusiveRangeValidator(0, 10),
        ])
        value = '-1'
        self.assertFalse(validator.validate(value))

    def test_any_validators_true(self):
        pass
