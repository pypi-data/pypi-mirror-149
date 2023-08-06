from unittest import TestCase
from meimbalance2.datalake.utils import split_datalake_url

class SplitTests(TestCase):
    def test_split_datalake_url(self):
        url = 'https://dls01.blob.core.windows.net/root/some/path/from/root/file.txt'

        directory, filename = split_datalake_url(url)

        self.assertEqual(filename, 'file.txt')
        self.assertEqual(directory, 'some/path/from/root')