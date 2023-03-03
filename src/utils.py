import os
from glob import glob

def list_images(path,recursive=False):
    """
        Returns a list of file paths
    """
    if not os.path.exists(path): raise Exception("folder not found")
    
    # Find Files
    results = []
    file_types = ("*.jpg", "*.jpeg", "*.png", "*.bmp")
    for file_type in file_types:
        results += glob(os.path.join(path, file_type), recursive=recursive)
    return map(lambda i: os.path.basename(i), results)

def change_file_ext(filepath, new_ext):
    """
        Returns a file path with new file extension
    """
    name, ext = os.path.splitext(filepath)
    
    # prefix a .
    if new_ext[0] != ".": new_ext = f".{new_ext}"
    
    # return
    return name + new_ext

def is_empty(file_path):
    """
        Returns true if the filesize equals to 0 bytes
    """
    return os.path.exists(file_path) and os.stat(file_path).st_size == 0