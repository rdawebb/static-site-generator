# imports
from enum import Enum

# enums
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

    # check if two text nodes are equal
    def __eq__(self, other):
        # compare text, type, and url
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
    
    # represent the text node as a string
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"