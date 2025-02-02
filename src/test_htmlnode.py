import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_tag(self):
        node = HTMLNode("b", "This is an HTML node")
        output = "<class 'htmlnode.HTMLNode'>(<b>This is an HTML node</b>)"
        self.assertEqual(str(node), output)
    
    def test_val(self):
        node = HTMLNode(value="This is an HTML node")
        output = "<class 'htmlnode.HTMLNode'>(<None>This is an HTML node</None>)"
        self.assertEqual(str(node), output)
    
    def test_props(self):
        props = {
            "href": "https://www.boot.dev",
            "target": "_blank",
        }
        node = HTMLNode("a", "This is an HTML node", props=props)
        output = '<class \'htmlnode.HTMLNode\'>(<a href="https://www.boot.dev" target="_blank">This is an HTML node</a>)'
        self.assertEqual(str(node), output)
    
    def test_children(self):
        props = {
            "href": "https://www.boot.dev",
            "target": "_blank",
        }
        children = [
            HTMLNode(value="This "),
            HTMLNode(tag="i", value="is a "),
            HTMLNode(tag="a", value="children ", props=props),
            HTMLNode(tag="b", value="test"),
        ]
        node = HTMLNode("p", children=children)
        output = "<class 'htmlnode.HTMLNode'>(<p>None"
        output += "\n  <class 'htmlnode.HTMLNode'>(<None>This </None>)"
        output += "\n  <class 'htmlnode.HTMLNode'>(<i>is a </i>)"
        output += "\n  <class 'htmlnode.HTMLNode'>(<a href=\"https://www.boot.dev\" target=\"_blank\">children </a>)"
        output += "\n  <class 'htmlnode.HTMLNode'>(<b>test</b>)"
        output += "\n</p>)"
        self.assertEqual(str(node), output)

if __name__ == "__main__":
    unittest.main()