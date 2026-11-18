import os

import pygame

_image_cache = {} # Cache for loaded images to avoid reloading them multiple times

# The assets folder is always next to this file, no matter where the game is launched from
ASSETS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

def find_asset(filename):
    """Return the full path to an asset file searching every subfolder of the assets folder"""
    for folder, subfolders, files in os.walk(ASSETS_PATH):
        if filename in files:
            return os.path.join(folder, filename)
    raise FileNotFoundError(f"File {filename} not found in {ASSETS_PATH}")

def load_image(filename, width=None):
    """ Load an image with transparency. If width is given, scale it to that width while keeping the aspect ratio. """
    key = (filename, width)
    if key not in _image_cache:
        image = pygame.image.load(find_asset(filename)).convert_alpha()
        if width is not None:
            # Scale the image to the given width while keeping the aspect ratio
            aspect_ratio = image.get_height() / image.get_width()
            new_height = int(width * aspect_ratio)
            image = pygame.transform.scale(image, (width, new_height))
        _image_cache[key] = image
    return _image_cache[key] 