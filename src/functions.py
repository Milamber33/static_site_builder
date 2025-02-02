import re
import shutil
import os
from textnode import TextType, TextNode
from leafnode import LeafNode
from parentnode import ParentNode


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url,"alt":text_node.text})
        case _:
            raise Exception("Invalid node type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for n in old_nodes:
        parent_type = n.text_type
        new_text = n.text.split(delimiter)
        if (
            len(new_text) % 2 == 1
            or (
                n.text[:len(delimiter)] != delimiter
                and n.text[-len(delimiter):] == delimiter
            )
            or (
                n.text[:len(delimiter)] == delimiter
                and n.text[-len(delimiter):] != delimiter
            )
        ):
            if(n.text[:len(delimiter)] == delimiter):
                new_type = text_type
            else:
                new_type = parent_type
            for t in new_text:
                if len(t) > 0:
                    new_nodes.append(TextNode(t, new_type))
                    if new_type == parent_type:
                        new_type = text_type
                    else:
                        new_type = parent_type
        else:
            print(n.text)
            raise Exception("Invalid markdown")
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        images = extract_markdown_images(n.text)
        remaining_text = n.text
        if len(images) > 0:
            for i in images:
                new_text = remaining_text.split(f"![{i[0]}]({i[1]})", 1)
                if len(new_text[0]) > 0:
                    new_nodes.append(TextNode(new_text[0], n.text_type))
                    remaining_text = remaining_text[len(new_text[0]):]
                new_nodes.append(TextNode(i[0], TextType.IMAGE, i[1]))
                remaining_text = remaining_text[len(i[0])+len(i[1])+5:]
            if len(remaining_text) > 0:
                new_nodes.append(TextNode(remaining_text, n.text_type))
        else:
            new_nodes.append(n)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        links = extract_markdown_links(n.text)
        remaining_text = n.text
        if len(links) > 0:
            for l in links:
                new_text = remaining_text.split(f"[{l[0]}]({l[1]})", 1)
                if len(new_text[0]) > 0:
                    new_nodes.append(TextNode(new_text[0], n.text_type))
                    remaining_text = remaining_text[len(new_text[0]):]
                new_nodes.append(TextNode(l[0], TextType.LINK, l[1]))
                remaining_text = remaining_text[len(l[0])+len(l[1])+4:]
            if len(remaining_text) > 0:
                new_nodes.append(TextNode(remaining_text, n.text_type))
        else:
            new_nodes.append(n)
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    output = []
    for b in blocks:
        b = b.strip()
        if len(b) > 0:
            output.append(b)
    return output

def block_to_block_type(block):
    headings = re.match(r"#{1,6} ", block)
    if headings:
        return f"h{len(headings[0])-1}"
    if block[:3] == block[-3:] == "```":
        return "code"
    lines = block.split("\n")
    blockquote = True
    for l in lines:
        if l[:2] != "> ":
            blockquote = False
    if blockquote:
        return "blockquote"
    ul = True
    for l in lines:
        if l[:2] != "* " and l[:2] != "- ":
            ul = False
    if ul:
        return "ul"
    ol = True
    i = 1
    for l in lines:
        if l[:len(str(i))+2] != f"{i}. ":
            ol = False
        i += 1
    if ol:
        return "ol"
    return "p"

def strip_block_tags(block, type):
    if type == 'p':
        return block
    if type[0] == 'h':
        return block[int(type[1])+1:]
    if type == 'code':
        return block[3:-3]
    lines = block.split("\n")
    new_lines = []
    if type == 'blockquote' or type == 'ul':
        for l in lines:
            new_lines.append(l[2:])
        return "\n".join(new_lines)
    if type == "ol":
        for l in lines:
            pos = l.find(".")
            new_lines.append(l[pos+2:])
        return "\n".join(new_lines)
    raise Exception("Unknown block type")


def markdown_to_html_node(markdown):
    blocks = []
    text_blocks = markdown_to_blocks(markdown)
    for t in text_blocks:
        block_type = block_to_block_type(t)
        if block_type == 'ol' or block_type == 'ul':
            lines = t.split("\n")
            items = []
            for l in lines:
                if len(l) > 0:
                    children = text_to_html_nodes(l, block_type)
                    items += children
            blocks.append(ParentNode(block_type, items))
        else:
            children = text_to_html_nodes(t, block_type)
            if block_type == "code":
                blocks.append(ParentNode('pre',children))
            else: 
                blocks += children
    return ParentNode('div', blocks)

def text_to_html_nodes(text, block_type):
    text_nodes = text_to_textnodes(strip_block_tags(text, block_type))
    children = []
    for t in text_nodes:
        if len(t.text) > 0:
            children.append(text_node_to_html_node(t))
    if block_type == "ul" or block_type == "ol":
        block_type = "li"
    return [ParentNode(block_type, children)]

def copy_dir(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    for item in os.listdir(src):
        path = os.path.join(src, item)
        if os.path.isdir(path):
            copy_dir(path, os.path.join(dest, item))
        else:
            shutil.copy(path, dest)

def extract_title(markdown):
    lines = markdown.split("\n")
    for l in lines:
        if l[:2] == "# ":
            return l[2:].strip()
        
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path)
    from_text = from_file.read()
    from_file.close()
    template_file = open(template_path)
    template_text = template_file.read()
    template_file.close()
    content = markdown_to_html_node(from_text).to_html()
    title = extract_title(from_text)
    dest_text = template_text.replace(r"{{ Title }}", title).replace(r"{{ Content }}", content)
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    dest_file = open(dest_path, "x")
    dest_file.write(dest_text)
    dest_file.close()

def generate_pages_recursive(from_dir, template_path, dest_dir):
    for item in os.listdir(from_dir):
        from_path = os.path.join(from_dir, item)
        if os.path.isdir(from_path):
            dest_path = os.path.join(dest_dir, item)
            generate_pages_recursive(from_path, template_path, dest_path)
        else:
            dest_path = os.path.join(dest_dir, item[:-3] + ".html")
            generate_page(from_path, template_path, dest_path)