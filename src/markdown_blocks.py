# import necessary modules
import re
from enum import Enum
from htmlnode import ParentNode
from split_nodes import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

# block types
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"

# function to convert markdown string to list of blocks
def markdown_to_blocks(markdown):
    # list to hold the final blocks
    final_blocks = []

    # split the markdown by double newlines to get separate blocks
    blocks = markdown.split("\n\n")
    
    # iterate through each block
    for block in blocks:
        block = block.strip() # trim whitespace
      
        # skip empty blocks
        if block == "":
            continue

        # add the block to final_blocks
        final_blocks.append(block)

    return final_blocks

# function to determine the block type based on its content
def block_to_block_type(block):
    # check if it's a heading block
    if is_heading_block(block):
        return BlockType.HEADING

    # check if it's a code block
    elif is_code_block(block):
        return BlockType.CODE

    # check if it's a quote block
    elif is_quote_block(block):
        return BlockType.QUOTE
    
    # check if it's an ordered list block
    elif is_ordered_list_block(block):
        return BlockType.ORDERED_LIST

    # check if it's an unordered list block
    elif is_unordered_list_block(block):
        return BlockType.UNORDERED_LIST

    # if not any other block type, it's a paragraph
    else:
        return BlockType.PARAGRAPH


# BLOCK TYPE HELPER FUNCTIONS

# helper function to check if a block is a heading block
def is_heading_block(block):
    return block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### "))

# regex to match opening code fence (` or ~)
code_fence_char = re.compile(r'^([`~])\1{2,}(?:\s|$)')

# helper function to check if a block is a code block
def is_code_block(block):
    # split the block into lines
    lines = block.splitlines()

    # check if the block is at least 2 lines 
    if len(lines) < 2:
        return False

    # check if the first line starts with at least 3 backticks or tildes - (` or ~)
    open = re.match(code_fence_char, lines[0])
    if not open:
        return False

    # check the fence character (` or ~)
    fence_char = open.group(1)

    # determine the length of the opening fence
    open_len = len(re.match(rf'^({re.escape(fence_char)}+)', lines[0]).group(1))

    # check if the last line has a matching closing fence of at least the same length
    return re.match(rf'^{re.escape(fence_char)}{{{open_len},}}\s*$', lines[-1]) is not None

# helper function to check if a block is a quote block
def is_quote_block(block):
    # split the block into lines
    lines = block.split("\n")

    # check if every line starts with >
    for line in lines:
        if not line.startswith(">"):
            return False # if any line does not start with >, it's not a quote
    return True

# helper function to check if a block is an ordered list block
def is_ordered_list_block(block):
    # split the block into lines
    lines = block.split("\n")

    # check if every line starts with 1 followed by a dot and a space, and increments correctly
    i = 1
    for line in lines:
        if not line.startswith(f"{i}. "):
            return False # if any line does not start with the expected number, it's not an ordered list
        i += 1
    return True

def is_unordered_list_block(block):
    # split the block into lines
    lines = block.split("\n")

    # check if every line starts with "- "
    for line in lines:
        if not line.startswith("- "):
            return False # if any line does not start with "- ", it's not an unordered list
    return True

# convert a markdown to an HTMLNodes
def markdown_to_html_node(markdown):
    # convert the markdown to blocks
    blocks = markdown_to_blocks(markdown)

    # convert each block to an HTMLNode and wrap in a ParentNode with tag "div"
    child_nodes = []
    for block in blocks:
        html_node = block_to_html_node(block)
        child_nodes.append(html_node)
    return ParentNode("div", child_nodes, None)

# convert a block to an HTMLNode
def block_to_html_node(block):
    # check the block type
    block_type = block_to_block_type(block)

    # check if it's a paragraph block
    if block_type == BlockType.PARAGRAPH:
        return paragraph_block_to_html_node(block)
    
    # check if it's a heading block
    elif block_type == BlockType.HEADING:
        return heading_block_to_html_node(block)
    
    # check if it's a code block
    elif block_type == BlockType.CODE:
        return code_block_to_html_node(block)
    
    # check if it's a quote block
    elif block_type == BlockType.QUOTE:
        return quote_block_to_html_node(block)
    
    # check if it's an ordered list block
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_block_to_html_node(block)
    
    # check if it's an unordered list block
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_block_to_html_node(block)
    
    # if not a valid block type, raise an error
    else:
        raise ValueError(f"Invalid block type: {block_type}")

# BLOCK TYPE TO HTML NODE HELPER FUNCTIONS

# function to convert text to child nodes
def text_to_child_nodes(text):
    # convert the text to text nodes
    text_nodes = text_to_textnodes(text)

    # convert each text node to an HTMLNode
    child_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        child_nodes.append(html_node)

    # return the list of child nodes
    return child_nodes

# convert a paragraph block to an HTMLNode
def paragraph_block_to_html_node(block):
    # split the block into lines
    lines = block.split("\n")
    
    # strip leading/trailing whitespace and join with a space
    for line in lines:
        line = line.strip()
    paragraph = " ".join(lines)

    # convert the paragraph text to child nodes
    child_nodes = text_to_child_nodes(paragraph)

    # return a ParentNode with tag "p" and the child nodes
    return ParentNode("p", child_nodes)

# convert a heading block to an HTMLNode
def heading_block_to_html_node(block):
    if not is_heading_block(block):
        raise ValueError("Invalid heading block")
    
    # check heading level by counting leading #
    match = re.match(r'^(#{1,6})\s+(.*)', block)

    # determine heading level
    level = len(match.group(1))

    # get the heading text
    heading_text = match.group(2).strip()

    # convert the heading text to child nodes
    child_nodes = text_to_child_nodes(heading_text)

    # return a ParentNode with the appropriate heading tag and child nodes
    return ParentNode(f"h{level}", child_nodes)

# convert a code block to an HTMLNode
def code_block_to_html_node(block):
    # if not a valid code block, raise an error
    if not is_code_block(block):
        raise ValueError("Invalid code block")
    
    # match the opening fence
    open = re.match(code_fence_char, block)
    fence_char = open.group(1)

    # strip the opening and closing fence characters
    code_text = re.sub(rf'^{re.escape(fence_char)}{{3,}}.*\n', '', block)
    code_text = re.sub(rf'\n{re.escape(fence_char)}{{3,}}\s*$', '', code_text)

    # create a TextNode for the code text and convert to HTMLNode
    code_node = TextNode(code_text, TextType.PLAIN)
    child = text_node_to_html_node(code_node)

    # return a ParentNode with tag "pre" containing a "code" child node
    return ParentNode("pre", [ParentNode("code", [child])])

# convert a quote block to an HTMLNode
def quote_block_to_html_node(block):
    # if not a valid quote block, raise an error
    if not is_quote_block(block):
        raise ValueError("Invalid quote block")
    
    # split the block into lines
    lines = block.split("\n")

    # remove leading > and any whitespace from each line and join with a space
    formatted_lines = []
    for line in lines:
        formatted_lines.append(line.lstrip(">").strip())
    quote_text = " ".join(formatted_lines)

    # convert the quote text to child nodes
    child_nodes = text_to_child_nodes(quote_text)

    # return a ParentNode with tag "blockquote" and the child nodes
    return ParentNode("blockquote", child_nodes)

# convert an ordered list block to an HTMLNode
def ordered_list_block_to_html_node(block):
    # if not a valid ordered list block, raise an error
    if not is_ordered_list_block(block):
        raise ValueError("Invalid ordered list block")
    
    # split the block into lines
    items = block.split("\n")
    
    # remove leading number and dot, convert to child nodes, and wrap in <li> tags
    list_items = []
    for item in items:
        item_text = re.sub(r"^\d+\.\s+", "", item)
        child_nodes = text_to_child_nodes(item_text)
        list_items.append(ParentNode("li", child_nodes))
    
    # return a ParentNode with tag "ol" and the list items
    return ParentNode("ol", list_items)

# convert an unordered list block to an HTMLNode
def unordered_list_block_to_html_node(block):
    # if not a valid unordered list block, raise an error
    if not is_unordered_list_block(block):
        raise ValueError("Invalid unordered list block")
    
    # split the block into lines
    items = block.split("\n")

    # remove leading "- " and space, convert to child nodes, and wrap in <li> tags
    list_items = []
    for item in items:
        item_text = item[2:].strip()
        child_nodes = text_to_child_nodes(item_text)
        list_items.append(ParentNode("li", child_nodes))
    return ParentNode("ul", list_items)