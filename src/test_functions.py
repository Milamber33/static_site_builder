import unittest

from functions import *


class TestFunctions(unittest.TestCase):
    def test_text(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        leaf_node = text_node_to_html_node(text_node)
        output = "This is a text node"
        self.assertEqual(leaf_node.to_html(), output)
    
    def test_bold(self):
        text_node = TextNode("This is a text node", TextType.BOLD)
        leaf_node = text_node_to_html_node(text_node)
        output = "<b>This is a text node</b>"
        self.assertEqual(leaf_node.to_html(), output)

    def test_italic(self):
        text_node = TextNode("This is a text node", TextType.ITALIC)
        leaf_node = text_node_to_html_node(text_node)
        output = "<i>This is a text node</i>"
        self.assertEqual(leaf_node.to_html(), output)

    def test_code(self):
        text_node = TextNode("This is a text node", TextType.CODE)
        leaf_node = text_node_to_html_node(text_node)
        output = "<code>This is a text node</code>"
        self.assertEqual(leaf_node.to_html(), output)

    def test_link(self):
        text_node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        leaf_node = text_node_to_html_node(text_node)
        output = "<a href=\"https://www.boot.dev\">This is a text node</a>"
        self.assertEqual(leaf_node.to_html(), output)

    def test_image(self):
        text_node = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev")
        leaf_node = text_node_to_html_node(text_node)
        output = "<img src=\"https://www.boot.dev\" alt=\"This is a text node\"></img>"
        self.assertEqual(leaf_node.to_html(), output)

    def test_split_text(self):
        text_node = TextNode("**This is a text node**", TextType.TEXT)
        output = [
            TextNode("This is a text node", TextType.BOLD),
        ]
        self.assertEqual(split_nodes_delimiter([text_node], "**", TextType.BOLD), output)

    def test_split_bold(self):
        text_node = TextNode("This is a **text** node", TextType.TEXT)
        output = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([text_node], "**", TextType.BOLD), output)

    def test_split_italic(self):
        text_node = TextNode("*This* is a text node", TextType.TEXT)
        output = [
            TextNode("This", TextType.ITALIC),
            TextNode(" is a text node", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([text_node], "*", TextType.ITALIC), output)

    def test_split_code(self):
        text_node = TextNode("This is a text `node`", TextType.TEXT)
        output = [
            TextNode("This is a text ", TextType.TEXT),
            TextNode("node", TextType.CODE),
        ]
        self.assertEqual(split_nodes_delimiter([text_node], "`", TextType.CODE), output)
    
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        output = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(extract_markdown_images(text), output)

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        output = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(extract_markdown_links(text), output)

    def test_split_iamges(self):
        node = TextNode(
            "![This](https://i.imgur.com/aKaOqIh.gif) is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        output = [
            TextNode("This", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(split_nodes_image([node]), output)

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        output = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(split_nodes_link([node]), output)
        
    def test_split_all(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), output)
    
    def test_split_blocks(self):
        text = "  # This is a heading\n\n\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n\n"
        output = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertEqual(markdown_to_blocks(text), output)
    
    def test_block_heading(self):
        tests = [
            ("This is a heading", "p"),
            ("# This is a heading", "h1"),
            ("## This is a heading", "h2"),
            ("### This is a heading", "h3"),
            ("#### This is a heading", "h4"),
            ("##### This is a heading", "h5"),
            ("###### This is a heading", "h6"),
            ("####### This is a heading", "p"),
        ]
        for t in tests:
            self.assertEqual(block_to_block_type(t[0]), t[1])
    
    def test_block_code(self):
        tests = [
            ("```This is code```", "code"),
            ("`This is code`", "p"),
            ("```This is code", "p"),
            ("This is code```", "p"),
        ]
        for t in tests:
            self.assertEqual(block_to_block_type(t[0]), t[1])

    def test_block_quote(self):
        tests = [
            (">This is a blockquote", "blockquote"),
            (">This\n>is\n>a\n>blockquote", "blockquote"),
            (">This\nis\na\nblockquote", "p"),
            ("This\n>is\n>a\n>blockquote", "p"),
        ]
        for t in tests:
            self.assertEqual(block_to_block_type(t[0]), t[1])

    def test_block_ul(self):
        tests = [
            ("*This is an unordered list", "ul"),
            ("*This\n*is\n*an\n*unordered\n*list", "ul"),
            ("-This is an unordered list", "ul"),
            ("-This\n-is\n-an\n-unordered\n-list", "ul"),
            ("-This\n*is\n*an\n-unordered\n-list", "ul"),
            ("This\n*is\n*an\n-unordered\n-list", "p"),
            ("-This\n*is\n*an\n-unordered\nlist", "p"),
        ]
        for t in tests:
            self.assertEqual(block_to_block_type(t[0]), t[1])

    def test_block_ol(self):
        tests = [
            ("1. This is an ordered list", "ol"),
            ("1. This\n2. is\n3. an\n4. ordered\n5. list", "ol"),
            ("1. This\n2. is\n3. an\n4. ordered\n5.list", "p"),
            ("1. This\n2. is\n3. an\n4. ordered\n3. list", "p"),
        ]
        for t in tests:
            self.assertEqual(block_to_block_type(t[0]), t[1])

    def test_full_process(self):
        test = """
# This is a heading

## This is another heading

###### This is a third heading


This is a paragraph of text. It has some **bold** and *italic* words inside of it.

*This is the first list item in a list block
*This is a list item
*This is another list item

1. This
2. is
3. a
4. really
5. really
6. very
7. stupidly
8. long
9. ordered
10. list

```This is
a code block```

>This is
>a blockquote

This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)
"""
        output = ParentNode('div', [
            ParentNode("h1", [LeafNode(None, "This is a heading")]),
            ParentNode("h2", [LeafNode(None, "This is another heading")]),
            ParentNode("h6", [LeafNode(None, "This is a third heading")]),
            ParentNode("p", [
                LeafNode(None, "This is a paragraph of text. It has some "),
                LeafNode("b", "bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
                LeafNode(None, " words inside of it."),
            ]),
            ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "This is the first list item in a list block")]),
                ParentNode("li", [LeafNode(None, "This is a list item")]),
                ParentNode("li", [LeafNode(None, "This is another list item")]),
            ]),
            ParentNode("ol", [
                ParentNode("li", [LeafNode(None, "This")]),
                ParentNode("li", [LeafNode(None, "is")]),
                ParentNode("li", [LeafNode(None, "a")]),
                ParentNode("li", [LeafNode(None, "really")]),
                ParentNode("li", [LeafNode(None, "really")]),
                ParentNode("li", [LeafNode(None, "very")]),
                ParentNode("li", [LeafNode(None, "stupidly")]),
                ParentNode("li", [LeafNode(None, "long")]),
                ParentNode("li", [LeafNode(None, "ordered")]),
                ParentNode("li", [LeafNode(None, "list")]),
            ]),
            ParentNode("pre", [ParentNode("code", [LeafNode(None, "This is\na code block")]),]),
            ParentNode("blockquote", [LeafNode(None, "This is\na blockquote")]),
            ParentNode("p", [
                LeafNode(None, "This is "),
                LeafNode("b", "text"),
                LeafNode(None, " with an "),
                LeafNode("i", "italic"),
                LeafNode(None, " word and a "),
                LeafNode("code", "code block"),
                LeafNode(None, " and an "),
                LeafNode("img", "", {"src":"https://i.imgur.com/fJRm4Vk.jpeg", "alt":"obi wan image"}),
                LeafNode(None, " and a "),
                LeafNode("a", "link", {"href":"https://boot.dev"}),
            ]),
        ])
        self.assertEqual(markdown_to_html_node(test).to_html(), output.to_html())

    def test_extract_title(self):
        test = """
# This is a heading

## This is another heading

###### This is a third heading


This is a paragraph of text. It has some **bold** and *italic* words inside of it.

*This is the first list item in a list block
*This is a list item
*This is another list item

1. This
2. is
3. a
4. really
5. really
6. very
7. stupidly
8. long
9. ordered
10. list

```This is
a code block```

>This is
>a blockquote

This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)
"""        
        output = "This is a heading"
        self.assertEqual(extract_title(test), output)

if __name__ == "__main__":
    unittest.main()