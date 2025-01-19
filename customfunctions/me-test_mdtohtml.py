import unittest
from mdtohtml import markdown_to_html_node
from parentnode import ParentNode

class TestMarkdownToHtmlNode(unittest.TestCase):
    
    def test_paragraph(self):
        markdown = "This is a simple paragraph."
        result = markdown_to_html_node(markdown)
        
        # Check the structure of the parent node and its child
        parent_node = result
        self.assertEqual(len(parent_node.children), 1)
        paragraph_node = parent_node.children[0]
        self.assertEqual(paragraph_node.tag, "p")
        self.assertEqual(paragraph_node.children[0].value, "This is a simple paragraph.")
        
    def test_heading(self):
        markdown = "# Heading 1"
        result = markdown_to_html_node(markdown)
        
        parent_node = result
        self.assertEqual(len(parent_node.children), 1)
        heading_node = parent_node.children[0]
        self.assertEqual(heading_node.tag, "h1")
        self.assertEqual(heading_node.children[0].value, "Heading 1")
        
    def test_blockquote(self):
        markdown = "> This is a blockquote."
        result = markdown_to_html_node(markdown)
        
        parent_node = result
        self.assertEqual(len(parent_node.children), 1)
        blockquote_node = parent_node.children[0]
        self.assertEqual(blockquote_node.tag, "blockquote")
        self.assertEqual(blockquote_node.children[0].value, "This is a blockquote.")
        
    def test_unordered_list(self):
        markdown = """
- Item 1
- Item 2
- Item 3
"""
        result = markdown_to_html_node(markdown)
        
        parent_node = result
        self.assertEqual(len(parent_node.children), 1)
        ul_node = parent_node.children[0]
        self.assertEqual(ul_node.tag, "ul")
        
        # Check each <li> inside <ul>
        self.assertEqual(len(ul_node.children), 3)
        self.assertEqual(ul_node.children[0].tag, "li")
        self.assertEqual(ul_node.children[0].children[0].value, "Item 1")
        
        self.assertEqual(ul_node.children[1].tag, "li")
        self.assertEqual(ul_node.children[1].children[0].value, "Item 2")
        
        self.assertEqual(ul_node.children[2].tag, "li")
        self.assertEqual(ul_node.children[2].children[0].value, "Item 3")
        
    def test_code_block(self):
        markdown = """```python
def my_function():
    return True
```"""
        result = markdown_to_html_node(markdown)
        
        parent_node = result
        self.assertEqual(len(parent_node.children), 1)
        pre_node = parent_node.children[0]
        self.assertEqual(pre_node.tag, "pre")
        
        code_node = pre_node.children[0]
        self.assertEqual(code_node.tag, "code")
        self.assertEqual(code_node.children[0].value, "def my_function():\n    return True")
