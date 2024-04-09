
from torch import Tensor
from torchvision.transforms import ToTensor
from PIL import Image

"""
Converts a given PIL image to a tensor
if the given image is a RGBA image (has alpha channel), it is converted to RGB prior
"""
def pil_to_tens(image: Image) -> Tensor:
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    return ToTensor()(image).unsqueeze(0).permute(0, 2, 3, 1)
