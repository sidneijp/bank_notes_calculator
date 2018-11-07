from collections import OrderedDict
from copy import copy
import sys


class InputValidator(object):
    error_message = 'A validation error occurred.'
    cast_type = None

    def __init__(self, cast_type=None):
        self.cast_type = cast_type

    def validate(self, value):
        pass

    def get_error_message(self, value):
        return self.error_message

    def cast(self, value):
        return self.cast_type(value) if self.cast_type else value


class InputEqualsValidator(InputValidator):
    error_message = 'Value "{v}" is not equal to {ev}.'

    def __init__(self, expected_value, cast_type=None):
        super().__init__(cast_type)
        self.expected_value = expected_value

    def validate(self, value):
        return self.expected_value == self.cast(value)

    def get_error_message(self, value):
        return self.error_message.format(v=value, ev=self.expected_value)


class InputInclusiveRangeValidator(InputValidator):
    error_message = 'Value "{v}" isn\'t greater than or equal to {l} nor lesser than or equal to {u}.'

    def __init__(self, lower, upper, cast_type=int):
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
    error_message = 'None of the validations passed. At least one should pass:\n'

    def __init__(self, validators, cast_type=None):
        super().__init__(cast_type)
        self.validators = validators

    def validate(self, value):
        return any([v.validate(value) for v in self.validators])

    def get_error_message(self, value):
        return self.error_message + '\n'.join(
            [v.get_error_message(value) for v in self.validators]
        )


class InputScanner(object):
    def __init__(self, stop_by=-1, data_stream=sys.stdin, prompt_message='',
                 validators=[], cast_type=int):
        self.stop_by = stop_by
        self.data_stream = data_stream
        self.prompt_message = prompt_message
        self.validators = validators
        self.cast_type = cast_type

    def __next__(self):
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
            raise StopIteration
        return self._value

    def __iter__(self):
        return self

    def cast(self, value):
        return self.cast_type(value) if self.cast_type else value


class BankNotesCollection(object):
    def __init__(self, available_bank_notes, bank_notes={}):
        self.available_bank_notes = tuple(filter(
            lambda x: x != None,
            available_bank_notes
        ))
        size = len(self.available_bank_notes)
        if bank_notes:
            self._bank_notes = bank_notes
        else:
            self._bank_notes = OrderedDict(
                zip(
                    self.available_bank_notes,
                    [0] * size
                )
            )

    @staticmethod
    def from_dict(bank_notes_dict):
        available_bank_notes = sorted(bank_notes_dict.keys(), reverse=True)
        return BankNotesCollection(available_bank_notes, bank_notes_dict)

    def to_dict(self):
        return self._bank_notes

    def get_available_bank_notes(self):
        return self.available_bank_notes


class BankNotesCalculator(object):
    def min_amount_bank_notes(self, bank_notes_collection, monetary_value):
        remaining_value = monetary_value
        bank_notes = copy(bank_notes_collection.to_dict())
        for bank_note, amount in bank_notes.items():
            bank_notes[bank_note] = remaining_value // bank_note
            remaining_value %= bank_note
        if bank_note and remaining_value > 0:
            bank_notes[bank_note] += 1
        return BankNotesCollection.from_dict(bank_notes)


class BankNotesCollectionFormatter(object):
    def __init__(self, pre_template='',
                 line_template='{} notas de {}\n',
                 post_template=''):
        self.pre_template = pre_template
        self.line_template = line_template
        self.post_template = post_template

    def __call__(self, collection):
        bank_notes = collection.to_dict()
        output = self.pre_template
        for bank_note, amount in bank_notes.items():
            output += self.line_template.format(amount, bank_note)
        output += self.post_template
        return output


def main():
    validators = [
        InputIntegerValidator(), InputOrValidator([
            InputInclusiveRangeValidator(1, 1000),
            InputEqualsValidator(-1, cast_type=int),
        ])
    ]
    bank_notes = tuple(InputScanner(prompt_message='input: ', validators=validators))

    print('')

    validators = [
        InputIntegerValidator(), InputOrValidator([
            InputInclusiveRangeValidator(0, 10000),
            InputEqualsValidator(-1, cast_type=int),
        ])
    ]
    for test_case in InputScanner(prompt_message='input: ', validators=validators):
        collection = BankNotesCollection(bank_notes, bank_notes=None)
        calculator = BankNotesCalculator()
        collection = calculator.min_amount_bank_notes(collection, test_case)
        formatter = BankNotesCollectionFormatter()
        print(formatter(collection))
    return True


if __name__ == '__main__':
    main()

