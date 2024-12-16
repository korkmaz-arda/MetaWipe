from PIL import Image
import os

SUPPORTED_TYPES = ['.jpg', '.jpeg']


def remove_metadata(file_path):
    with Image.open(file_path) as img:
        img_format = img.format
        img.save(file_path, format=img_format)


def clean_dir(dir):
    for root, _, files in os.walk(dir):
        for file in files:
            if os.path.splitext(file)[1].lower() in SUPPORTED_TYPES:
                remove_metadata(os.path.join(root, file))
