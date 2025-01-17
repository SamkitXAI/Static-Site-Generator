from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if not self.tag :
            raise ValueError("Each parent should have a tag")
        if not self.children:
            raise ValueError("Each child node should have values")
        
        
        children_html = "".join(child.to_html() if isinstance(child, HTMLNode) else "" for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"     