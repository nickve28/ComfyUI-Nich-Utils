

import time
import uuid
from server import PromptServer
import os
import re
import random
from PIL import Image

from .utils.file_utils import filename_without_extension, list_images
from .utils.tensor_utils import pil_to_tens

class ImageFromDirSelector:
    def __init__(self) -> None:
        self.current_image = None
        self.current_tensor = None
        seed = int.from_bytes(os.urandom(4), 'big') + int(time.time() * 1000)
        self.random_number_generator = random.Random(seed)

    CATEGORY = 'Nich/utils'
    RETURN_TYPES = ("IMAGE", "STRING", "STRING",)
    RETURN_NAMES = ("image", "filename", "filename_without_extension",)

    FUNCTION = "sample_images"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": ("STRING", { "default": "~/images" }),
                "keep_current_selection": ("BOOLEAN", { "default": False }),
                "selected_image_name": ("STRING", { "multiline": True }),
                "include_subdirectories": ("BOOLEAN", { "default": False }),
            },
            "optional": {
                "regexp_filter": ("STRING", { "default": None, "multiline": True })
            },
            "hidden": {"unique_id": "UNIQUE_ID"}
        }

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return kwargs['selected_image_name'] if kwargs['keep_current_selection'] else str(uuid.uuid1())


    def get_current_image(self, selected_image_name):
        return selected_image_name if selected_image_name else self.current_image


    def requires_new_image(self, current_image, keep_current_selection):
        return not current_image or not keep_current_selection


    def get_files(self, full_path, regexp_filter, include_subdirectories):
        filename_filter_regexp = None
        if regexp_filter:
            filename_filter_regexp = re.compile(regexp_filter)

        return list_images(full_path, include_subdirectories, filename_filter_regexp)


    def sample_images(self, directory, unique_id, keep_current_selection=False, selected_image_name=None, regexp_filter=None,include_subdirectories=False):
        full_path = os.path.expanduser(directory)
        prior_selected_image = self.get_current_image(selected_image_name)
        new_image = prior_selected_image
        new_image_required = self.requires_new_image(prior_selected_image, keep_current_selection)
        if new_image_required:
            image_files = self.get_files(full_path, regexp_filter, include_subdirectories)
            self.current_image = self.random_number_generator.choice(image_files)
            new_image = self.current_image

        PromptServer.instance.send_sync("nich-image-selected", {"node_id": unique_id, "value": new_image})

        if new_image_required or self.current_tensor is None:
            image = Image.open(os.path.join(full_path, new_image))
            self.current_tensor = pil_to_tens(image).unsqueeze(0)

        return self.current_tensor, self.current_image, filename_without_extension(self.current_image)


NODE_CLASS_MAPPINGS = {
    "Image from Dir Selector (Nich)": ImageFromDirSelector
}
