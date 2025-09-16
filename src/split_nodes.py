# import necessary modules
import re
from textnode import TextNode, TextType

# function to covert text into list of approptiate nodes
def text_to_textnodes(text):
    # start with a single plain text node
    nodes = [TextNode(text, TextType.PLAIN)]
    
    # split by various markdown syntaxes
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # split by link markdown
    nodes = split_nodes_link(nodes)
    
    # split by image markdown
    nodes = split_nodes_image(nodes)

    # return the final list of text nodes
    return nodes


# function to split text nodes by a given delimiter
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = [] # list to hold the new text nodes
    
    # iterate through each old text node
    for node in old_nodes:
        # if the node is not of type PLAIN, keep it unchanged
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        # if the node text is empty, raise error
        if not node.text:
            raise ValueError(f"Node text is empty")
        
        # if the delimiter is not in the text, keep the node unchanged
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        
        # if delimiter is empty, raise error
        if delimiter == "":
            raise ValueError("Delimiter cannot be empty")

        # split the text by the delimiter
        parts = node.text.split(delimiter)
        
        # check if the number of parts is even, which indicates unmatched delimiters
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown - unmatched delimiter '{delimiter}' in text: {node.text}")

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

# function to split text nodes to extract markdown image links
def split_nodes_image(old_nodes):
    new_nodes = [] # list to hold the new text nodes
    
    # iterate through each old text node
    for node in old_nodes:
        # if the node is not of type PLAIN, keep it unchanged
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        # if the node text is empty, raise error
        if not node.text:
            raise ValueError(f"Node text is empty")
        
        # store copy of the original text
        original_text = node.text

        # extract all markdown image links from the copy
        images = extract_markdown_images(original_text)

        # if no images found, keep the node unchanged
        if not images:
            new_nodes.append(node)
            continue
        
        # iterate through each found image
        for image in images:
            # split the original text by the first occurrence of the image markdown
            parts = original_text.split(f"![{image[0]}]({image[1]})", 1)

            # check if the number of parts is not 2, which indicated the markdown is not properly closed
            if len(parts) != 2:
                raise ValueError(f"Invalid markdown - image part not closed: {original_text}")

            # check if the plain text before the image is not empty
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.PLAIN)) # plain text before the image

            # add the image text node
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            # update original to the remaining text after the image
            original_text = parts[1]

        # after processing all images, add any remaining plain text as a new node
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN)) # plain text after the image
            original_text = "" # clear original to avoid duplicate addition

    # return the list of new text nodes
    return new_nodes

# function to split text nodes to extract markdown links
def split_nodes_link(old_nodes):
    new_nodes = [] # list to hold the new text nodes
    
    # iterate through each old text node
    for node in old_nodes:
        # if the node is not of type PLAIN, keep it unchanged
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        # if the node text is empty, raise error
        if not node.text:
            raise ValueError(f"Node text is empty")

        # store copy of the original text
        original_text = node.text

        # extract all markdown links from the copy
        links = extract_markdown_links(original_text)

        # if no links found, keep the node unchanged
        if not links:
            new_nodes.append(node)
            continue
        
        # iterate through each found link
        for link in links:
            # split the original text by the first occurrence of the link markdown
            parts = original_text.split(f"[{link[0]}]({link[1]})", 1)

            # check if the number of parts is not 2, which indicated the markdown is not properly closed
            if len(parts) != 2:
                raise ValueError(f"Invalid markdown - link part not closed: {original_text}")

            # check if the plain text before the link is not empty
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.PLAIN)) # plain text before the link

            # add the link text node
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            # update original to the remaining text after the link
            original_text = parts[1]

        # after processing all links, add any remaining plain text as a new node
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN)) # plain text after the link
            original_text = "" # clear original to avoid duplicate addition

    # return the list of new text nodes
    return new_nodes

# function to extract markdown image links from text
def extract_markdown_images(text):
    
    # regex pattern to match markdown image links
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    
    # find all matches in the text
    return re.findall(pattern, text)

# function to extract markdown links from text
def extract_markdown_links(text):
   
    # regex pattern to match markdown links
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    
    # find all matches in the text
    return re.findall(pattern, text)