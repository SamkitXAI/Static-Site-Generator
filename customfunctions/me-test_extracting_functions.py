import unittest
from custom_funcs import extract_markdown_images, extract_markdown_links


class TestMarkdownFunctions(unittest.TestCase):

    # Tests for extract_markdown_images
    def test_extract_markdown_images_basic(self):
        text = "![alt text](https://example.com/image.png)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("alt text", "https://example.com/image.png")])

    def test_extract_markdown_images_multiple(self):
        text = "![image1](https://img1.png) and ![image2](https://img2.png)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("image1", "https://img1.png"), ("image2", "https://img2.png")])

    def test_extract_markdown_images_no_images(self):
        text = "This is a test with no images."
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [])

    # Tests for extract_markdown_links
    def test_extract_markdown_links_basic(self):
        text = "[alt text](https://www.google.com)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("alt text", "https://www.google.com")])

    def test_extract_markdown_links_multiple(self):
        text = "[link1](https://example1.com) and [link2](https://example2.com)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("link1", "https://example1.com"), ("link2", "https://example2.com")])

    def test_extract_markdown_links_no_links(self):
        text = "This is a test string with no links."
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [])

    def test_extract_markdown_links_ignore_images(self):
        text = "![alt text](https://example.com/image.png) and [regular link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("regular link", "https://example.com")])

    def test_extract_markdown_links_nested_brackets(self):
        text = "[nested [text]](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [])
        
        
        
from textnode import TextNode, TextType
from custom_funcs import split_nodes_image, split_nodes_link


class TestSplitNodes(unittest.TestCase):

    # Tests for split_nodes_image
    def test_split_nodes_image_basic(self):
        node = TextNode("![alt text](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")],
        )

    def test_split_nodes_image_with_text(self):
        node = TextNode(
            "This is text with ![alt text](https://example.com/image.png) in it.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" in it.", TextType.TEXT),
            ],
        )

    def test_split_nodes_image_no_images(self):
        node = TextNode("This text has no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    # Tests for split_nodes_link
    def test_split_nodes_link_basic(self):
        node = TextNode("[alt text](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [TextNode("alt text", TextType.LINK, "https://example.com")],
        )

    def test_split_nodes_link_with_text(self):
        node = TextNode(
            "This is text with a [link](https://example.com) in it.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" in it.", TextType.TEXT),
            ],
        )

    def test_split_nodes_link_no_links(self):
        node = TextNode("This text has no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_link_ignore_images(self):
        node = TextNode(
            "![alt text](https://example.com/image.png) and [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("![alt text](https://example.com/image.png) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
        )
        
        
from custom_funcs import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_basic_text(self):
        text = "This is plain text"
        result = text_to_textnodes(text)
        expected = [TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_bold_text(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_italic_text(self):
        text = "This is *italic* text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_code_text(self):
        text = "This is `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_image_text(self):
        text = "This is an ![image](https://example.com/image.jpg)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
        ]
        self.assertEqual(result, expected)

    def test_link_text(self):
        text = "This is a [link](https://example.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)

    def test_combined_text(self):
        text = "This is **bold**, *italic*, `code`, an ![image](https://example.com/image.jpg), and a [link](https://example.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(", and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)
        
