from PIL import Image
import os

SUPPORTED_TYPES = ['.jpg', '.jpeg', '.png']


def strip_metadata(file_path):
    with Image.open(file_path) as img:
        img.save(file_path, format=img.format, exif=None)
    print(f"Removed metadata from: {file_path}")


def clean_dir(dir):
    for root, _, files in os.walk(dir):
        for file in files:
            if os.path.splitext(file)[1].lower() in SUPPORTED_TYPES:
                strip_metadata(os.path.join(root, file))
    print("Metadata cleaning complete.")
