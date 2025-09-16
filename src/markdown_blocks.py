# import necessary modules
import re
from enum import Enum

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


# HELPER FUNCTIONS

# helper function to check if a block is a heading block
def is_heading_block(block):
    return block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### "))

# helper function to check if a block is a code block
def is_code_block(block):
    # split the block into lines
    lines = block.splitlines()

    # check if the block is at least 2 lines 
    if len(lines) < 2:
        return False

    # check if the first line starts with at least 3 backticks or tildes - (` or ~)
    open = re.match(r'^([`~])\1{2,}(?:\s|$)', lines[0])
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