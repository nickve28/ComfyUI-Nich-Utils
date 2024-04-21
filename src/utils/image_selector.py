import os
import random
import re
import time
from tkinter import Image

from utils.file_utils import list_images
from utils.tensor_utils import pil_to_tens

class ImageSelector():
    def __init__(self):
        self._current_image = None
        self._current_tensor = None
        seed = int.from_bytes(os.urandom(4), 'big') + int(time.time() * 1000)
        self._random_number_generator = random.Random(seed)
    
    def cycle_image(self, directory, selected_image_path, include_subdirectories, regexp_filter):
        self.directory = directory
        self.full_path = os.path.expanduser(directory)
        self.selected_image_path = selected_image_path

        filename_filter_regexp = None
        if regexp_filter:
            filename_filter_regexp = re.compile(regexp_filter)
        image_files = list_images(self.full_path, include_subdirectories, filename_filter_regexp)
        selected_image_file = self._random_number_generator.choice(image_files)
        (selected_image_file, self.current_image(), self.current_tensor())
    
    def current_tensor(self):
        if not self._current_tensor:
            self._current_tensor = pil_to_tens(self.current_image())
        return self._current_image

    def current_image(self):
        if not self._current_image:
            self._current_image = Image.open(os.path.join(self.full_path, self.selected_image_path))
