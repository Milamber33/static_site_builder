class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("TODO")

    def props_to_html(self):
        html = ""
        if self.props != None:
            for p in self.props:
                html += f' {p}="{self.props[p]}"'
        return html
    
    def __repr__(self):
        output = f"{type(self)}(<{self.tag}{self.props_to_html()}>{self.value}"
        if self.children != None:
            for c in self.children:
                output += f"\n  {c}"
            output += "\n"
        output += f"</{self.tag}>)"
        return output