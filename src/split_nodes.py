# import the necessary modules and classes
from textnode import TextNode, TextType

# function to split text nodes by a given delimiter
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = [] # list to hold the new text nodes
    
    # iterate through each old text node
    for node in old_nodes:
        # if the node is not of type PLAIN, keep it unchanged
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        # if the node text is empty, raise exception
        if not node.text:
            raise Exception(f"Node text is empty")

        # if the delimiter is empty, raise exception
        if not delimiter:
            raise Exception(f"Delimiter is empty")

        # if matching delimiter not found, raise exception
        if delimiter not in node.text:
            raise Exception(f"Delimiter '{delimiter}' not found in text: {node.text}")
        
        # split the text by the delimiter
        parts = node.text.split(delimiter)
        
        # check if the number of parts is even, which indicates unmatched delimiters
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")

        # iterate through the parts and create new text nodes
        for i in range(len(parts)):
            # skip empty parts
            if parts[i] == "":
                continue
            # even index parts are plain text, odd index parts are of the specified text type
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.PLAIN)) # plain text
            else:
                new_nodes.append(TextNode(parts[i], text_type)) # text with the specified type

    # return the list of new text nodes
    return new_nodes