# import necessary modules
import logging
from copy_directory import copy_directory
from generate_content import generate_page_recursive

# configure logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# main function
def main():
    # log the start of the site generation process
    logging.info("Starting site generation...")
    
    # define destination directories
    static_path = "./static"
    public_path = "./public"

    # define source directories and files
    content_path = "./content"
    template_path = "./template.html"

    # copy contents from static directory to public directory
    logging.info("Clearing public directory and copying static files...")
    copy_directory(static_path, public_path)
    logging.info("Static files copied successfully.")

    # generate HTML page from markdown file using template
    logging.info("Generating HTML pages from markdown content...")
    generate_page_recursive(content_path, template_path, public_path)
    
    # confirm the completion of the site generation process
    logging.info("Site generation completed successfully.")

# run main function if this script is executed
if __name__ == "__main__":
    main()