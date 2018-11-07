from collections import OrderedDict
from copy import copy

from inputs import (InputEqualsValidator, InputIntegerValidator,
                    InputOrValidator, InputInclusiveRangeValidator,
                    InputScanner,)


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

