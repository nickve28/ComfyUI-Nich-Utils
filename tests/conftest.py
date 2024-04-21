import os
import sys

# Get the root directory of the project
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))

# Add the root directory to the Python path
sys.path.insert(0, root_dir)
