
import numpy as np
from torch import Tensor
import torch
from torchvision.transforms import ToTensor
from PIL import Image

"""
Converts a given PIL image to a tensor
if the given image is a RGBA image (has alpha channel), it is converted to RGB prior
"""
def pil_to_tens(image: Image) -> Tensor:
    output = image.convert("RGB")
    output = np.array(output).astype(np.float32) / 255.0
    return torch.from_numpy(output)[None,]
