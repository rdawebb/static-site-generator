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
        return "".join(f' {key}="{value}"' for key, value in self.props.items())
    
    # represent the html node as a string
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"