import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_children_repr(self):
        props = {
            "href": "https://www.boot.dev",
            "target": "_blank",
        }
        level_2 = [
            LeafNode("u", "is "),
            LeafNode("s", "a "),
        ]
        children = [
            LeafNode(None, "This "),
            ParentNode("i", level_2),
            LeafNode("a", "children ", props),
            LeafNode("b", "test"),
        ]
        node = ParentNode("p", children)
        output = "<class 'parentnode.ParentNode'>(<p>None"
        output += "\n  <class 'leafnode.LeafNode'>(<None>This </None>)"
        output += "\n  <class 'parentnode.ParentNode'>(<i>None"
        output += "\n  <class 'leafnode.LeafNode'>(<u>is </u>)"
        output += "\n  <class 'leafnode.LeafNode'>(<s>a </s>)"
        output += "\n</i>)"
        output += "\n  <class 'leafnode.LeafNode'>(<a href=\"https://www.boot.dev\" target=\"_blank\">children </a>)"
        output += "\n  <class 'leafnode.LeafNode'>(<b>test</b>)"
        output += "\n</p>)"
        self.assertEqual(str(node), output)

    def test_children_to_html(self):
        props = {
            "href": "https://www.boot.dev",
            "target": "_blank",
        }
        level_2 = [
            LeafNode("u", "is "),
            LeafNode("s", "a "),
        ]
        children = [
            LeafNode(None, "This "),
            ParentNode("i", level_2),
            LeafNode("a", "children ", props),
            LeafNode("b", "test"),
        ]
        node = ParentNode("p", children)
        output = "<p>This <i><u>is </u><s>a </s></i><a href=\"https://www.boot.dev\" target=\"_blank\">children </a><b>test</b></p>"
        self.assertEqual(node.to_html(), output)

if __name__ == "__main__":
    unittest.main()