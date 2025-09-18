# import necessary modules
import os
import re
from markdown_blocks import markdown_to_html_node, markdown_to_blocks, is_heading_block

# generate a complete HTML page from a markdown file using a template
def generate_page(from_path, template_path, dest_path):
    # check if source markdown file exists
    if not os.path.exists(from_path) or not os.path.isfile(from_path):
        raise ValueError(f"Markdown file does not exist: {from_path}")

    # check if template file exists
    if not os.path.exists(template_path) or not os.path.isfile(template_path):
        raise ValueError(f"Template file does not exist: {template_path}")

    # check if destination path exists and is a directory
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir) or not os.path.isdir(dest_dir):
        raise ValueError(f"Destination path is not a valid directory: {dest_dir}")

    # confirm the page generation action
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}...")
    
    # read the markdown file
    with open(from_path, "r", encoding="utf-8") as markdown_file:
        markdown = markdown_file.read()

    # read the template file
    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()

    # extract the title from the markdown content
    title = extract_title(markdown)

    # convert the markdown content to an HTMLNode
    html_node = markdown_to_html_node(markdown)
    if html_node is None:
        raise ValueError("Error converting markdown to HTMLNode")

    # convert to an HTML string
    content = html_node.to_html()

    # replace placeholders in template file with actual title and content
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    # write the final HTML to the destination file
    try:
        with open(dest_path, "w", encoding="utf-8") as dest_file:
            dest_file.write(final_html)
    # handle any errors during file writing
    except Exception as e:
        raise IOError(f"Error writing to destination file: {dest_path} - {e}")

    # confirm successful generation of the page
    print(f"Page generated successfully: {dest_path}")

# extract the title (H1 heading) from a markdown string
def extract_title(markdown):
    # split the markdown into blocks
    blocks = markdown_to_blocks(markdown)

    # iterate through the blocks to find the title
    for block in blocks:
        if is_heading_block(block):
            # extract and return the heading text without leading #
            return re.sub(r'^(#{1})\s*(.*?)(\n|$)', r'\2', block).strip()

    # if no title found, raise an error
    raise ValueError("No title (H1) found in markdown")