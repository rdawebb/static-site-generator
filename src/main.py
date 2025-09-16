# import necessary modules
from textnode import TextNode, TextType

# main function
def main():
    # create a text node with dummy data
    node = TextNode("Hello, World!", TextType.LINK, "http://example.com")

    # print the text node
    print(node)

# run main function if this script is executed
if __name__ == "__main__":
    main()