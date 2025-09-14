# html class for representing html nodes
class HTMLNode:
    # constructor
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    # convert to html string
    def to_html(self):
        raise NotImplementedError
    
    # convert properties to html string
    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())
    
    # represent the html node as a string
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    # constructor
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, [], props)

    # convert to html string
    def to_html(self):
        # check for value
        if self.value is None:
            raise ValueError("LeafNode must have a value") # raise error if no value
        # check for tag
        if self.tag is None:
            return self.value # return value as plain text if no tag
        # return html string
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"