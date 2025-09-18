# import necessary modules
import os
import re
import logging
from markdown_blocks import markdown_to_html_node, markdown_to_blocks, is_heading_block

# configure logging for debugging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("generate_content.log"), logging.StreamHandler()])

# recursively generate HTML pages from markdown files in a directory using a template
def generate_page_recursive(content_dir, template_path, dest_dir):
    # check if content path exists and is a directory
    if not os.path.exists(content_dir) or not os.path.isdir(content_dir):
        logging.error(f"Content does not exist or is not a directory: {content_dir}")
        return

    # check if template file exists
    if not os.path.exists(template_path) or not os.path.isfile(template_path):
        logging.error(f"Template file does not exist: {template_path}")
        return

    # check if destination path exists and is a directory
    if not os.path.exists(dest_dir) or not os.path.isdir(dest_dir):
        logging.error(f"Destination directory does not exist or is not a directory: {dest_dir}")
        return

    # log the start of the page generation process
    logging.info(f"Generating pages from {content_dir} to {dest_dir} using template {template_path}...")

    # iterate over files and directories in the content directory
    for file in os.listdir(content_dir):
        # skip hidden files and directories
        if file.startswith('.'):
            continue
        
        # define full paths for content and destination
        content_path = os.path.join(content_dir, file)
        dest_path = os.path.join(dest_dir, file)

        # if content is a directory, recurse into it
        if os.path.isdir(content_path):
            # create the corresponding directory in the destination path
            try:
                os.makedirs(dest_path, exist_ok=True)
            # handle any errors during directory creation
            except Exception as e:
                logging.error(f"Error creating directory: {dest_path} - {e}")
                continue
            
            # recurse into the directory    
            generate_page_recursive(content_path, template_path, dest_path)
        
        # if content is a file, generate a page from it
        else:
            dest_file_path = os.path.splitext(dest_path)[0] + ".html"
            
            # generate the HTML page
            try:
                generate_page(content_path, template_path, dest_file_path)
            # handle any errors during page generation
            except Exception as e:
                logging.error(f"Error generating page for {content_path}: {e}")

# generate a complete HTML page from a markdown file using a template
def generate_page(markdown_path, template_path, dest_path):
    # check if source markdown file exists
    if not os.path.exists(markdown_path) or not os.path.isfile(markdown_path):
        logging.error(f"Markdown file does not exist: {markdown_path}")
        return

    # check if destination path exists and is a directory
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir) or not os.path.isdir(dest_dir):
        logging.error(f"Destination path is not a valid directory: {dest_dir}")
        return

    # confirm the page generation action
    logging.info(f"Generating page from {markdown_path} to {dest_path} using template {template_path}...")

    # read the markdown file
    with open(markdown_path, "r", encoding="utf-8") as markdown_file:
        markdown = markdown_file.read()

    # read the template file
    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()

    # extract the title from the markdown content
    title = extract_title(markdown)

    # convert the markdown content to an HTMLNode
    html_node = markdown_to_html_node(markdown)
    if html_node is None:
        logging.error("Error converting markdown to HTMLNode")
        return

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
        logging.error(f"Error writing to destination file: {dest_path} - {e}")
        return

    # confirm successful generation of the page
    logging.info(f"Page generated successfully: {dest_path}")

# extract the title (H1 heading) from a markdown string
def extract_title(markdown):
    # split the markdown into blocks
    blocks = markdown_to_blocks(markdown)

    # iterate through the blocks to find the title
    for block in blocks:
        if is_heading_block(block):
            # extract and return the heading text without leading #
            return re.sub(r'^#\s+(.*?)(\n|$)', r'\1', block).strip()

    # if no title found, raise an error
    raise ValueError("No title (H1) found in markdown")