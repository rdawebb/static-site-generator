# import necessary modules
from enum import Enum
from htmlnode import LeafNode

# text types
class TextType(Enum):
    PLAIN = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

# text node class
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    # function to check if two text nodes are equal
    def __eq__(self, other):
        # compare text, type, and url
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)

    # function to represent the text node as a string
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

# function to convert text node to corresponding html node
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.PLAIN:
        return LeafNode(None, text_node.text) # plain text has no tag
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text) # bold text uses <b> tag
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text) # italic text uses <i> tag
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text) # code text uses <code> tag
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url}) # link text uses <a> tag with href
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text}) # image uses <img> tag with src and alt text
    else:
        raise Exception(f"Invalid text type: {text_node.text_type}") # raise error for unknown type