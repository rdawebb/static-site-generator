# import necessary modules
from copy_directory import copy_directory

# main function
def main():
    # define source and destination directories
    source_dir = "static"
    dest_dir = "public"

    # copy contents from source directory to destination directory
    copy_directory(source_dir, dest_dir)

# run main function if this script is executed
if __name__ == "__main__":
    main()