from bank_notes import (BankNotesCalculator, BankNotesCollection,
                        BankNotesCollectionFormatter)
from inputs import (InputEqualsValidator, InputIntegerValidator,
                    InputOrValidator, InputInclusiveRangeValidator,
                    InputScanner,)


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

