import unittest
from custom_funcs import markdown_to_blocks, block_to_block_type


class TestMarkdownToBlocks(unittest.TestCase):

    # Test case for basic markdown with no empty lines
    def test_markdown_to_blocks_basic(self):
        markdown = "This is a test.\nAnother line of text."
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["This is a test. Another line of text."])

    # Test case for markdown with multiple blocks separated by empty lines
    def test_markdown_to_blocks_multiple_blocks(self):
        markdown = "First block.\n\nSecond block."
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["First block.", "Second block."])

    # Test case for markdown with leading/trailing whitespace and empty lines
    def test_markdown_to_blocks_with_whitespace(self):
        markdown = "   Leading spaces\n\nTrailing spaces   "
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["Leading spaces", "Trailing spaces"])

    # Test case for markdown with multiple empty lines
    def test_markdown_to_blocks_multiple_empty_lines(self):
        markdown = "Block 1.\n\n\nBlock 2."
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["Block 1.", "Block 2."])

    # Test case for markdown with only empty lines
    def test_markdown_to_blocks_empty_input(self):
        markdown = "\n\n\n"
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, [])


class TestMarkdownBlockTypes(unittest.TestCase):
    def test_heading_block(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), "heading")

    def test_code_block(self):
        block = "```\ndef hello_world():\n    print('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_quote_block(self):
        block = "> This is a quote\n> It spans multiple lines"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_unordered_list_block(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_ordered_list_block(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_paragraph_block(self):
        block = "This is a normal paragraph without any special formatting."
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_invalid_ordered_list(self):
        block = "1. First item\n3. Second item\n4. Third item"
        self.assertEqual(block_to_block_type(block), "paragraph")  # Incorrect numbering

    def test_mixed_list_block(self):
        block = "1. Ordered item\n- Unordered item"
        self.assertEqual(block_to_block_type(block), "paragraph")  # Mixed list types

    def test_incomplete_code_block(self):
        block = "```\ndef hello_world():\n    print('Hello, world!')"
        self.assertEqual(block_to_block_type(block), "paragraph")  # No closing ```

    def test_incomplete_heading(self):
        block = "###Heading without space"
        self.assertEqual(block_to_block_type(block), "paragraph")  # No space after ###
