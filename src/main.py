# import necessary modules
import os
from copy_directory import copy_directory
from generate_content import generate_page

# main function
def main():
    # define destination directories
    static_path = "./static"
    public_path = "./public"

    # define source directories and files
    content_path = "./content"
    template_path = "./template.html"

    # copy contents from static directory to public directory
    copy_directory(static_path, public_path)

    # generate HTML page from markdown file using template
    generate_page(os.path.join(content_path, "index.md"), template_path, os.path.join(public_path, "index.html"))

# run main function if this script is executed
if __name__ == "__main__":
    main()