import os
import re

from typing import Optional

SUPPORTED_IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.webp']

def file_matches_filter(relative_file_path: str, filter_regex: Optional[str]):
    if not any(relative_file_path.endswith(ext) for ext in SUPPORTED_IMAGE_EXTENSIONS):
        return False
    return True if not filter_regex else re.search(filter_regex, relative_file_path)

"""
This function lists all images in the given path, with the extensions jpg, jpeg, png and webp
Allows searching in subdirectories as well, and constraining output to files matching the provided optional regular expression
"""
def list_images(full_path: str, include_subdirectories: bool, filename_filter_regexp: str=None):
    files_list = []
    for root, _, files in os.walk(full_path):
        for file_name in files:
            relative_path = os.path.relpath(os.path.join(root, file_name), full_path)

            if file_matches_filter(relative_path, filename_filter_regexp):
                files_list.append(relative_path)

        if not include_subdirectories:
            break

    return files_list


"""
Strips the extension from the provided filename
eg: heaven.png will return heaven
"""
def filename_without_extension(filename):
    return os.path.splitext(filename)[0]