import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_tag_repr(self):
        node = LeafNode("b", "This is a leaf node")
        output = "<class 'leafnode.LeafNode'>(<b>This is a leaf node</b>)"
        self.assertEqual(str(node), output)

    def test_tag_to_html(self):
        node = LeafNode("b", "This is a leaf node")
        output = "<b>This is a leaf node</b>"
        self.assertEqual(node.to_html(), output)
    
    def test_val_repr(self):
        node = LeafNode(None, "This is a leaf node")
        output = "<class 'leafnode.LeafNode'>(<None>This is a leaf node</None>)"
        self.assertEqual(str(node), output)
    
    def test_val_to_html(self):
        node = LeafNode(None, "This is a leaf node")
        output = "This is a leaf node"
        self.assertEqual(node.to_html(), output)

    def test_props_repr(self):
        props = {
            "href": "https://www.boot.dev",
            "target": "_blank",
        }
        node = LeafNode("a", "This is a leaf node", props)
        output = '<class \'leafnode.LeafNode\'>(<a href="https://www.boot.dev" target="_blank">This is a leaf node</a>)'
        self.assertEqual(str(node), output)
    
    def test_props_to_html(self):
        props = {
            "href": "https://www.boot.dev",
            "target": "_blank",
        }
        node = LeafNode("a", "This is a leaf node", props)
        output = '<a href="https://www.boot.dev" target="_blank">This is a leaf node</a>'
        self.assertEqual(node.to_html(), output)

if __name__ == "__main__":
    unittest.main()