import os
import shutil

def clear_directory(directory):
    # Check if the directory exists
    if os.path.exists(directory):
        # Loop through all files and subdirectories in the directory
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)  # Remove file
                    print(f"Deleted file: {item_path}")
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # Remove directory and its contents
                    print(f"Deleted directory: {item_path}")
            except Exception as e:
                print(f"Error deleting {item_path}: {e}")
    else:
        print(f"Directory does not exist: {directory}")

# Directories to clear
directories_to_clear = ['./audio', './scenes', './transcript']

for directory in directories_to_clear:
    clear_directory(directory)

print("All specified directories have been cleared.")
