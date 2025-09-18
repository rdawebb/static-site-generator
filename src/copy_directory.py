# import necessary modules
import os
import shutil
import logging

# configure logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# clear contents of existing directory
def clear_directory(directory):
    
    # check if directory exists
    if os.path.exists(directory) and os.path.isdir(directory):
        # log the clearing action
        logging.info(f"Clearing directory: {directory}")
        
        # iterate over items in the directory and remove them
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            try:
                # if item is a directory, remove it recursively, else remove the file
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
            
            # log any errors encountered during removal
            except Exception as e:
                logging.error(f"Error removing item: {item_path} - {e}")

        # log the completion of the clearing action
        logging.info(f"Completed clearing directory: {directory}")
    
    # if directory does not exist, log a warning
    else:
        logging.warning(f"Directory does not exist: {directory} - nothing to clear.")

# copy contents from source directory to destination directory
def copy_directory(source, destination):
    # if source directory does not exist or is not a directory, log an error
    if not os.path.exists(source) or not os.path.isdir(source):
        logging.error(f"Source directory does not exist or is not a directory: {source}")
        return
      
    # if destination directory exists, clear it, else create it
    if os.path.exists(destination) and os.path.isdir(destination):
        clear_directory(destination)
    else:
        os.makedirs(destination, exist_ok=True)
    
    # iterate over items in the source directory and copy them to the destination
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        # if item is a directory, copy it recursively
        if os.path.isdir(source_path):
            os.makedirs(destination_path, exist_ok=True)
            copy_directory(source_path, destination_path)

        # if item is a symlink, replicate the symlink
        elif os.path.islink(source_path):
            link_target = os.readlink(source_path)

            # only create the symlink if the target exists
            if os.path.exists(link_target):
                os.symlink(link_target, destination_path)
                logging.info(f"Copied symlink: {source_path} to {destination_path}")
            else:
                logging.warning(f"Symlink does not exist: {link_target} - skipping symlink: {source_path}")
        
        # if item is a file, copy it
        else:
            try:
                shutil.copy2(source_path, destination_path)
                # log the file copying for debugging
                logging.info(f"Copied file: {source_path} to {destination_path}")
            
            # log any errors encountered during file copying
            except Exception as e:
                logging.error(f"Error copying file: {source_path} to {destination_path} - {e}")