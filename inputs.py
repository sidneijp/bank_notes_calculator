import sys


class InputValidator(object):
    '''Base class for input validators.'''

    error_message = 'A validation error occurred.'
    cast_type = None

    def __init__(self, cast_type=None):
        '''
        - cast_type: for better flexibility with values a cast_type can be passed
        to cast the value being validated.
        '''
        self.cast_type = cast_type

    def validate(self, value):
        pass

    def get_error_message(self, value):
        return self.error_message

    def cast(self, value):
        return self.cast_type(value) if self.cast_type else value


class InputEqualsValidator(InputValidator):
    '''Validates if the input is equal to the expected_value.'''

    error_message = 'Value "{v}" is not equal to {ev}.'

    def __init__(self, expected_value, cast_type=None):
        '''
        - expected_value: value compared with the input being validated.
        - cast_type: for better flexibility with values a cast_type can be passed
        to cast the value being validated.
        '''
        super().__init__(cast_type)
        self.expected_value = expected_value

    def validate(self, value):
        return self.expected_value == self.cast(value)

    def get_error_message(self, value):
        return self.error_message.format(v=value, ev=self.expected_value)


class InputInclusiveRangeValidator(InputValidator):
    '''Validates if the input is inside an inclusive range (a <= x <= z).'''

    error_message = 'Value "{v}" isn\'t greater than or equal to {l} nor lesser than or equal to {u}.'

    def __init__(self, lower, upper, cast_type=int):
        '''
        - lower: numerical lower range limit
        - upper: numerical upper range limit
        - cast_type: for better flexibility with values a cast_type can be passed
        to cast the value being validated.
        '''
        super().__init__(cast_type)
        self.lower = lower
        self.upper = upper

    def validate(self, value):
        return self.lower <= self.cast(value) <= self.upper

    def get_error_message(self, value):
        return self.error_message.format(v=value, l=self.lower, u=self.upper)


class InputIntegerValidator(InputValidator):
    error_message = 'Value "{v}" is not an integer.'

    def validate(self, value):
        try:
            int(value)
        except:
            return False
        return True

    def get_error_message(self, value):
        return self.error_message.format(v=value)


class InputOrValidator(InputValidator):
    '''Validator to group validators using OR logic for their validations results.'''

    error_message = 'None of the validations passed. At least one should pass:\n'

    def __init__(self, validators, cast_type=None):
        '''
        - validators: list of validators whose the OR logic is applied to.
        It's also used to build the error message.
        - cast_type: for better flexibility with values a cast_type can be passed
        to cast the value being validated.
        '''
        super().__init__(cast_type)
        self.validators = validators

    def validate(self, value):
        return any([v.validate(value) for v in self.validators])

    def get_error_message(self, value):
        return self.error_message + '\n'.join(
            [v.get_error_message(value) for v in self.validators]
        )


class InputScanner(object):
    '''Class used to read inputs from a data stream as an iterator.'''

    def __init__(self, stop_by=-1, data_stream=sys.stdin, prompt_message='',
                 validators=[], cast_type=int):
        '''
        - stop_by: value to stop reading user's input
        - data_stream: stream used to read data from. e.g. stdin, StrinIO, etc.
        - prompt_message: message showed before the user's input
        - validators: list of validations applied for each value inputed by the
        user. If the value doesn't pass though the validations the iterator
        iterator returns `None` so it can be easiy filtered.
        - cast_type: after validations, the value is casted using the value of
        this parameter. None indicate no cast to be applied.
        '''
        self.stop_by = stop_by
        self.data_stream = data_stream
        self.prompt_message = prompt_message
        self.validators = validators
        self.cast_type = cast_type
        self._stopped = False

    def __next__(self):
        if self._stopped:
            raise StopIteration
        if self.prompt_message:
            print(self.prompt_message, end='', flush=True)
        self._value = next(self.data_stream)
        self._value = self._value.strip('\n')
        for validator in self.validators:
            if not validator.validate(self._value):
                print(validator.get_error_message(self._value))
                return
        self._value = self.cast(self._value)
        if self._value == self.stop_by:
            self._stopped = True
            raise StopIteration
        return self._value

    def __iter__(self):
        return self

    def cast(self, value):
        return self.cast_type(value) if self.cast_type else value

