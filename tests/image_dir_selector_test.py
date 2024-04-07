import pytest
from torch import Tensor

from src.nodes import ImageFromDirSelector

# Setup / Helpers
def fixture_file_path():
    "../fixtures/files"
# Tests

def test_image_dir_selector_loads_image(mocker):
    node = ImageFromDirSelector()
    result = node.sample_images(fixture_file_path(), "1", False)
    assert isinstance(result, Tensor)