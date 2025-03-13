from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("invalid HTML: no tag")
        if self.children == None:
            raise ValueError("invalid HTML: no children")
        output = f"<{self.tag}{self.props_to_html()}>"
        for c in self.children:
            output += c.to_html()
        output += f"</{self.tag}>"
        return output
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"