# import necessary modules
import logging
import sys
from copy_directory import copy_directory
from generate_content import generate_page_recursive

# configure logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# main function
def main():
    # determine the base path of the script
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    # normalise base path
    if not base_path.endswith('/'):
        base_path = base_path + '/'
    if not base_path.startswith('/'):
        base_path = '/' + base_path

    logging.info(f"Base path: {base_path}")
    
    # log the start of the site generation process
    logging.info("Starting site generation...")
    
    # define destination directories
    static_path = "./static"
    dest_path = "./docs"

    # define source directories and files
    content_path = "./content"
    template_path = "./template.html"

    # copy contents from static directory to destination directory
    logging.info("Clearing destination directory and copying static files...")
    copy_directory(static_path, dest_path)
    logging.info("Static files copied successfully.")

    # generate HTML page from markdown file using template
    logging.info("Generating HTML pages from markdown content...")
    generate_page_recursive(content_path, template_path, dest_path, base_path)

    # confirm the completion of the site generation process
    logging.info("Site generation completed successfully.")

# run main function if this script is executed
if __name__ == "__main__":
    main()