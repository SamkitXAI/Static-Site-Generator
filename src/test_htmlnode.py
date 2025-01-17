import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a paragraph")
        node2 = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node, node2)
    
    def test_props(self):
        node = HTMLNode("p", "This is a paragraph", props={"class": "paragraph"})
        self.assertEqual(node.props, {"class": "paragraph"})
        
    def test_props_to_html(self):
        node = HTMLNode("p", "This is a paragraph", props={"class": "paragraph"})
        self.assertEqual(node.props_to_html(), ' class="paragraph"')
        
    def test_props_custom(self):
        props = {"class": "paragraph", "id": "first"}
        node = HTMLNode("p", "This is a paragraph", props=props)
        self.assertEqual(node.props, props)


if __name__ == "__main__":
    unittest.main()