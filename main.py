import sys

from bank_notes import (BankNotesCalculator, BankNotesCollection,
                        BankNotesCollectionFormatter)
from inputs import (InputEqualsValidator, InputIntegerValidator,
                    InputOrValidator, InputInclusiveRangeValidator,
                    InputScanner,)


def main(data_stream):
    validators = [
        InputIntegerValidator(), InputOrValidator([
            InputInclusiveRangeValidator(1, 1000),
            InputEqualsValidator(-1, cast_type=int),
        ])
    ]
    scanner = InputScanner(
        prompt_message='input: ', validators=validators,
        data_stream=data_stream
    )
    bank_notes = tuple(scanner)

    print('')

    validators = [
        InputIntegerValidator(), InputOrValidator([
            InputInclusiveRangeValidator(0, 10000),
            InputEqualsValidator(-1, cast_type=int),
        ])
    ]

    scanner = InputScanner(
        prompt_message='input: ', validators=validators,
        data_stream=data_stream
    )
    formatter = BankNotesCollectionFormatter()
    calculator = BankNotesCalculator()
    for test_case in scanner:
        collection = BankNotesCollection(bank_notes, bank_notes=None)
        collection = calculator.min_amount_bank_notes(collection, test_case)
        print(formatter(collection))
    return True


if __name__ == '__main__':
    main(sys.stdin)

