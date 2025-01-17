import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "This is a paragraph")
        node2 = LeafNode("p", "This is a paragraph")
        self.assertEqual(node, node2)
    
    def test_props(self):
        node = LeafNode("p", "This is a paragraph", props={"class": "paragraph"})
        self.assertEqual(node.props, {"class": "paragraph"})
        
    def test_props_to_html(self):
        node = LeafNode("p", "This is a paragraph", props={"class": "paragraph"})
        self.assertEqual(node.props_to_html(), ' class="paragraph"')
        
    def test_props_custom(self):
        props = {"class": "paragraph", "id": "first"}
        node = LeafNode("p", "This is a paragraph", props=props)
        self.assertEqual(node.props, props)
    
    def test_not_tag(self):
        node = LeafNode(None, "This is a paragraph")
        self.assertEqual(node.to_html(), "This is a paragraph")
        
    def test_boot_dev(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
    
    def test_boot_devs(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        
    


if __name__ == "__main__":
    unittest.main()