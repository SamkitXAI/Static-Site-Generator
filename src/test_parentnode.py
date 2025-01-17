import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):

    def test_nesting_parent_nodes(self):
        # ParentNode with nested children
        node = ParentNode("div", [
            ParentNode("ul", [
                LeafNode("li", "Item 1"),
                LeafNode("li", "Item 2")
            ]),
            LeafNode("p", "This is a paragraph.")
        ])
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>Item 1</li><li>Item 2</li></ul><p>This is a paragraph.</p></div>"
        )

    def test_multiple_children(self):
        # ParentNode with multiple children (LeafNodes only)
        node = ParentNode("div", [
            LeafNode("h1", "Heading"),
            LeafNode("p", "A paragraph."),
            LeafNode("span", "Inline text.")
        ])
        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading</h1><p>A paragraph.</p><span>Inline text.</span></div>"
        )


    def test_missing_tag(self):
        # ParentNode missing tag
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "Some text")]).to_html()

    def test_missing_child_value(self):
        # LeafNode missing value
        with self.assertRaises(ValueError):
            ParentNode("div", [LeafNode("p", None)]).to_html()

    def test_props_to_html(self):
        # ParentNode with properties
        node = ParentNode("div", [
            LeafNode("p", "Text with props.")
        ], props={"class": "container", "id": "main"})
        self.assertEqual(node.to_html(),'<div class="container" id="main"><p>Text with props.</p></div>')


    def test_empty_props(self):
        # ParentNode with empty props
        node = ParentNode("div", [LeafNode("p", "Text.")], props={})
        self.assertEqual(node.to_html(), "<div><p>Text.</p></div>")

    def test_deep_nesting(self):
        # Deeply nested ParentNode
        node = ParentNode("section", [
            ParentNode("article", [
                ParentNode("div", [
                    LeafNode("h1", "Deeply nested heading"),
                    LeafNode("p", "Nested paragraph")
                ])
            ])
        ])
        self.assertEqual(
            node.to_html(),
            "<section><article><div><h1>Deeply nested heading</h1><p>Nested paragraph</p></div></article></section>"
        )

    def test_single_leaf_node(self):
        # Single LeafNode with no ParentNode
        node = LeafNode("h1", "Just a heading")
        self.assertEqual(node.to_html(), "<h1>Just a heading</h1>")

    def test_empty_node(self):
        # ParentNode with no tag and no children
        with self.assertRaises(ValueError):
            ParentNode(None, []).to_html()



if __name__ == "__main__":
    unittest.main()
