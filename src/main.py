# importing the necessary modules
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from split_nodes import split_nodes_delimiter

# main function
def main():
    # create a text node with dummy data
    node = TextNode("Hello, World!", TextType.LINK, "http://example.com")

    # create a html node with dummy data
    html_node = HTMLNode("div", "Hello", [], {"class": "container"})

    # create a leaf node with dummy data
    leaf_node = LeafNode("a", "This is a link.", {"href": "http://example.com"})

    # create a parent node with a child leaf node with dummy data
    child_leaf = LeafNode("span", "Child text", {"class": "child"})
    parent_node = ParentNode("div", [child_leaf], {"class": "parent"})

    # create a dummy list of text nodes to split
    old_nodes = [TextNode("This is **bold** text", TextType.PLAIN)]
    # split the nodes by the bold delimiter
    new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

    # print the test nodes
    print(node)
    print(html_node)
    print(leaf_node)
    print(leaf_node.to_html())
    print(parent_node)
    print(parent_node.to_html())
    print(new_nodes)

# run main function if this script is executed
if __name__ == "__main__":
    main()