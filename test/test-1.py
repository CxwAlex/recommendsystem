# encoding=utf-8
import unittest

from pdfextractor.page import PdfPage

class PdfExtractorTest(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
