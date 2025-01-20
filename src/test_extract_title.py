import unittest
from inline_markdown import extract_title  # Replace with your actual module name

class TestExtractTitle(unittest.TestCase):
    def test_valid_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_h1_with_whitespace(self):
        self.assertEqual(extract_title("  #  Hello World  "), "Hello World")

    def test_no_h1(self):
        with self.assertRaises(ValueError):
            extract_title("No H1 header here.")

    def test_multiple_h1(self):
        self.assertEqual(extract_title("# First H1\n# Second H1"), "First H1")

if __name__ == "__main__":
    unittest.main()
