import torch
import numpy as np
from torchvision.transforms import ToTensor

import os
import random
from PIL import Image

def pil_to_tens(image):
    to_tensor = ToTensor()
    tensor = to_tensor(image).unsqueeze(0).permute(0, 2, 3, 1)
    return tensor

class ImageFromDirSelector:
    CATEGORY = 'Nich/utils'
    RETURN_TYPES = ("IMAGE", "STRING",)
    RETURN_NAMES = ("images", "selected_image_names",)

    FUNCTION = "sample_images"

    OUTPUT_IS_LIST = (True, True,)
    WEB_DIRECTORY = "./javascript"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": ("STRING", { "default": "/" }),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "amount_of_images": ("INT", { "default": 1, "min": 0, "max": 0xffffffffffffffff }),
                "keep_current_selection": ("BOOLEAN", { "default": False }),
                "selected_image_names": ("STRING", { "multiline": True, "dynamicPrompts": False })
            },
        }
    
    @classmethod
    def IS_CHANGED(self, directory, seed, amount_of_images, keep_current_selection, selected_images_names=""):
        return not keep_current_selection
    
    def get_images_as_torch_images(self, directory, sampled_image_names):
        output_images = []
        for sampled_image_name in sampled_image_names:
            image = Image.open(os.path.join(directory, sampled_image_name))
            output_images.append(pil_to_tens(image).unsqueeze(0))
        return output_images

    def sample_images(self, directory, seed, amount_of_images, keep_current_selection=False, selected_image_names=""):
        files = os.listdir(directory)
        image_files = [file for file in files if file.endswith(('.png', '.jpg', '.jpeg', 'webp'))]

        random.seed(seed)
        sampled_image_names = random.sample(image_files, amount_of_images)
        print(sampled_image_names)

        output_images = self.get_images_as_torch_images(directory, sampled_image_names)
        
        return (output_images, sampled_image_names,)


NODE_CLASS_MAPPINGS = {
    "Image from Dir Selector (Nich)": ImageFromDirSelector
}

