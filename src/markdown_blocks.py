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