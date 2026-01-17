from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError()
        if self.children is None or len(self.children) == 0:
            raise ValueError("No children")
        child_strs = []
        for child in self.children:
            child_strs.append(child.to_html())
        child_str = "".join(child_strs)
        return f"<{self.tag}{self.props_to_html()}>{child_str}</{self.tag}>"