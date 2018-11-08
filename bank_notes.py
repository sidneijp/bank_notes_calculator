from collections import OrderedDict
from copy import copy


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

    def __getitem__(self, key):
        return self._bank_notes[key]

    def __contains__(self, k):
        return k in self._bank_notes

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
                 line_template='{a} notas de {n}\n',
                 post_template=''):
        self.pre_template = pre_template
        self.line_template = line_template
        self.post_template = post_template

    def __call__(self, collection):
        bank_notes = collection.to_dict()
        output = self.pre_template
        for bank_note, amount in bank_notes.items():
            output += self.line_template.format(a=amount, n=bank_note)
        output += self.post_template
        return output
