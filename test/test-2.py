# encoding=utf-8
import unittest
import os

from book.cf2 import *
from test import test_data

class CfTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        filepath = os.path.join(os.path.dirname(__file__), '../pdfs/table.pdf')
        cls.extractor = StockFinanceExtractor(filepath)

    def test_get_tables(self):
        tables = self.extractor.get_tables()
        self.assertEqual(len(tables), 6)  # One of a table is not normalized. Now result is 17; right answer is 16
        table_row_lengths = [13, 8, 29, 4, 11, 4]
        # result = []
        for i, table in enumerate(tables):
            # print table
            self.assertEqual(len(table.rows), table_row_lengths[i])
            # result.append(str(len(table.rows)))
        # print(', '.join(result))

    def test_tables(self):
        tables = self.extractor.get_tables()
        table = tables[0]
        row_lengths = [5, 5, 5, 5, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        for i, row in enumerate(table.rows):
            self.assertEqual(len(row.cells), row_lengths[i])


if __name__ == '__main__':
    unittest.main()
