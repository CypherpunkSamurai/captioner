import os
from glob import glob

def list_images(path,recursive=False):
    """
        Returns a list of file paths
    """
    if not os.path.exists(path): raise Exception("folder not found")
    
    # Find Files
    results = []
    for file in glob(os.path.join(path, "*.jpg"), recursive=recursive):
        results.append(os.path.basename(file))
    return results

def change_file_ext(filepath, new_ext):
    """
        Returns a file path with new file extension
    """
    name, ext = os.path.splitext(filepath)
    
    # prefix a .
    if new_ext[0] != ".": new_ext = f".{new_ext}"
    
    # return
    return name + new_ext