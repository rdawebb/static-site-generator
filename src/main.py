# importing the necessary modules
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from htmlnode import LeafNode

# main function
def main():
    # create a text node with dummy data
    node = TextNode("Hello, World!", TextType.LINK, "http://example.com")

    # create a html node with dummy data
    html_node = HTMLNode("div", "Hello", [], {"class": "container"})

    # create a leaf node with dummy data
    leaf_node = LeafNode("a", "This is a link.", {"href": "http://example.com"})

    # print the test nodes
    print(node)
    print(html_node)
    print(leaf_node)
    print(leaf_node.to_html())

# run main function if this script is executed
if __name__ == "__main__":
    main()