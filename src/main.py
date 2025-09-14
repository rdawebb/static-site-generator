# importing the necessary modules
from textnode import TextNode, TextType
from htmlnode import HTMLNode

# main function
def main():
    # create a text node with dummy data
    node = TextNode("Hello, World!", TextType.LINK, "http://example.com")

    # create a html node with dummy data
    html_node = HTMLNode("div", "Hello", [], {"class": "container"})

    # print the test nodes
    print(node)
    print(html_node)

# run main function if this script is executed
if __name__ == "__main__":
    main()