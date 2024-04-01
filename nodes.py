import torch
import numpy as np
from torchvision.transforms import ToTensor

from server import PromptServer
import os
import random
from PIL import Image

def pil_to_tens(image):
    to_tensor = ToTensor()
    tensor = to_tensor(image).unsqueeze(0).permute(0, 2, 3, 1)
    return tensor

class ImageFromDirSelector:
    def __init__(self):
        self.current_image = None

    CATEGORY = 'Nich/utils'
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)

    FUNCTION = "sample_images"

    OUTPUT_IS_LIST = (False,)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": ("STRING", { "default": "~/images" }),
                "keep_current_selection": ("BOOLEAN", { "default": False }),
                "selected_image_name": ("STRING", { "multiline": True, "dynamicPrompts": False })
            },
            "hidden": {"unique_id": "UNIQUE_ID"}
        }
    
    @classmethod
    def IS_CHANGED(cls, _directory, keep_current_selection, unique_id):
        # TODO
        return not keep_current_selection

    def sample_images(self, directory, unique_id, keep_current_selection=False, selected_image_name=None):
        full_path = os.path.expanduser(directory)
        files = os.listdir(full_path)

        sampled_image_name = self.current_image or selected_image_name
        if (not sampled_image_name) or (not keep_current_selection):
            image_files = [file for file in files if file.endswith(('.png', '.jpg', '.jpeg', 'webp'))]
            sampled_image_name = random.choice(image_files) 
            self.current_image = sampled_image_name
          
        image = Image.open(os.path.join(full_path, sampled_image_name))
        PromptServer.instance.send_sync("nich-image-selected", {"node_id": unique_id, "value": sampled_image_name})
        
        return pil_to_tens(image).unsqueeze(0)

NODE_CLASS_MAPPINGS = {
    "Image from Dir Selector (Nich)": ImageFromDirSelector
}

