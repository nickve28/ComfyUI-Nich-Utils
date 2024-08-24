# Nich Comfy Utils

**This library is still in early development! It will likely contain bugs or oddities**

This library contains utility nodes for comfyUI.

## Image from Dir Selector

### Breaking change
- This node no longer contains the 'selected image' text box. This one was very unstable when loading / running multiple workflows. Please connect a text output to the filename output(s) if you want to retain what image was used in your workflow. This change should make it more idiomatic and reliable to use.

This node will select a random image from the provided  folder. It allows for
- Pinning a single image (if you want to keep using the selected image).
- Allows searching within subdirectories of the given directory path (optional).
- Filtering on a regular expression, for if you want to sample specific files only (optional).

### Example Use cases:
- Selecting a random image for IPadapter
- Cycling controlnet poses
- Cycling only through a subset of images (regular expression knowledge required).

## Select Text with Regular Expression

This node allows selecting parts of text using a regular expression, with a delimiter (default = whitespace)

### Example Use cases:
- Select a subset of a prompt

# Open work
- Improve code
- Add tests
- More nodes!
