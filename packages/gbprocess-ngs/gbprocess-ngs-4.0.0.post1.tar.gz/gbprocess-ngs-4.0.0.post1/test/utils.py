import unittest


class CustomTestCase(unittest.TestCase):
    def assertFileContentEquals(self, file_to_check, contents):
        with file_to_check.open("r") as fh:
            file_contents = fh.read().strip()
            self.assertMultiLineEqual(file_contents, contents)
