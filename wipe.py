from PIL import Image
import os

SUPPORTED_TYPES = ['.jpg', '.jpeg', '.png', '.svg', '.gif', '.bmp', '.tiff', '.webp']


def strip_metadata(file_path, output_path=None, verbose=True):
    with Image.open(file_path) as img:  
        img.save(output_path or file_path, format=img.format, exif=None)
    
    output_msg = f"-> Saved to: {output_path}" if output_path else ""
    if verbose:
        print(f"Removed metadata from: {file_path} {output_msg}")


def type_is_supported(file, supported_types=None):
    supported_types = supported_types or SUPPORTED_TYPES
    return os.path.splitext(file)[1].lower() in supported_types


def clean_dir(dir, output_dir=None, verbose=True):
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, _, files in os.walk(dir):
        for file in files:
            if type_is_supported(file):
                file_path = os.path.join(root, file)
                if output_dir:
                    output_path = file_path.replace(dir, output_dir, 1)
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                else:
                    output_path = file_path
                strip_metadata(file_path, output_path=output_path, verbose=verbose)
                
    print("Metadata cleaning complete.")
