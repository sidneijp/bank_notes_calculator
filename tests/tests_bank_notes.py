from collections import OrderedDict
from io import StringIO
import re
import unittest

from bank_notes import (BankNotesCalculator, BankNotesCollection,
                        BankNotesCollectionFormatter)


class TestBankNotesCalculator(unittest.TestCase):
    def test_min_amount_bank_notes(self):
        notes = [50, 30, 1]
        value = 134
        collection = BankNotesCollection(notes)
        calculator = BankNotesCalculator()
        collection = calculator.min_amount_bank_notes(
            collection, value
        )
        self.assertEqual(collection[50], 2)
        self.assertEqual(collection[30], 1)
        self.assertEqual(collection[1], 4)


class TestBankNotesCollection(unittest.TestCase):
    def test_object_construction(self):
        notes = [50, 30, 1]
        collection = BankNotesCollection(notes)

        self.assertTrue(50 in collection)
        self.assertTrue(30 in collection)
        self.assertTrue(1 in collection)

        self.assertEqual(collection[50], 0)
        self.assertEqual(collection[30], 0)
        self.assertEqual(collection[1], 0)

    def test_from_dict(self):
        bank_notes_dict = OrderedDict([
            (50, 2),
            (30, 1),
            (1, 4),
        ])

        collection = BankNotesCollection.from_dict(bank_notes_dict)

        self.assertTrue(50 in collection)
        self.assertTrue(30 in collection)
        self.assertTrue(1 in collection)

        self.assertEqual(collection[50], 2)
        self.assertEqual(collection[30], 1)
        self.assertEqual(collection[1], 4)


    def test_to_dict(self):
        bank_notes_dict = OrderedDict([
            (50, 2),
            (30, 1),
            (1, 4),
        ])

        collection = BankNotesCollection.from_dict(bank_notes_dict)

        self.assertEqual(collection.to_dict(), bank_notes_dict)


class TestBankNotesCollectionFormatter(unittest.TestCase):
    def test_output_formatting(self):
        bank_notes_dict = OrderedDict([
            (50, 2),
            (30, 1),
            (1, 4),
        ])

        collection = BankNotesCollection.from_dict(bank_notes_dict)

        formatter = BankNotesCollectionFormatter(
            pre_template='prepended',
            line_template='results (note: {n}, amount: {a})',
            post_template='apended',
        )

        output = formatter(collection)

        self.assertIsNotNone(re.search(r'^prepend', output, re.RegexFlag.MULTILINE))
        self.assertIsNotNone(re.search(r'results', output, re.RegexFlag.MULTILINE))
        self.assertIsNotNone(re.search(r'\d+', output, re.RegexFlag.MULTILINE))
        self.assertIsNotNone(re.search(r'apended$', output, re.RegexFlag.MULTILINE))
