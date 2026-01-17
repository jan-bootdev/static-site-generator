
class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError()
    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        tags = []
        for tag, value in self.props.items():
            tags.append(f"{tag}=\"{value}\"")
        return " " + " ".join(tags)
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children},{self.props})"