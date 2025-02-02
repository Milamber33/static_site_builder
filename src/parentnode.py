from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent nodes must have a tag")
        if self.children == None:
            raise ValueError("Parent nodes must have children")
        output = f"<{self.tag}{self.props_to_html()}>"
        for c in self.children:
            output += c.to_html()
        output += f"</{self.tag}>"
        return output