from PIL import Image
import os

MPEG1_ext = ['.mpg', '.mpeg']
JPEG_ext = ['.jpg', '.jpeg']
JPEG2000_ext = ['.jp2', '.j2k', '.jpc', '.jpf', '.jpx', '.j2c']

SUPPORTED_FORMATS = ['.png', *MPEG1_ext, *JPEG_ext, *JPEG2000_ext, 
                     '.svg', '.gif', '.bmp', '.tiff', '.webp', 
                     '.heif', 'heic', '.psd', '.pdf']


def strip_metadata(file_path, output_path=None, verbose=True, dry_run=False, backup=False):
    if dry_run:
        print(f"[DRY RUN] Would remove metadata from: {file_path}")
        return

    with Image.open(file_path) as img:  
        if not any(key in img.info for key in ["exif", "icc_profile", "text"]):
            if verbose:
                print(f"Skipping {file_path} (No metadata present).")
            return

        if backup:
            backup_path = file_path + ".bak"
            img.save(backup_path)
            if verbose:
                print(f"Backup saved: {backup_path}")

        img.save(output_path or file_path, format=img.format, exif=None)
    
    save_msg = f"-> Saved to: {output_path}" if output_path else ""
    if verbose:
        print(f"Removed metadata from: {file_path} {save_msg}")


def format_is_supported(file, custom_format_filter=None):
    supported_formats = custom_format_filter or SUPPORTED_FORMATS
    return os.path.splitext(file)[1].lower() in supported_formats


def clean_dir(target_dir, output_dir=None, verbose=True, dry_run=False, backup=False):
    if dry_run:
        print("[DRY RUN] Scanning directory:", target_dir)

    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, _, files in os.walk(target_dir):
        for file in files:
            if format_is_supported(file):
                file_path = os.path.join(root, file)

                if output_dir:
                    output_path = file_path.replace(target_dir, output_dir, 1)
                    if not dry_run:
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)
                else:
                    output_path = file_path
                strip_metadata(file_path, output_path=output_path, verbose=verbose, dry_run=dry_run, backup=backup)
                
    print("Metadata cleaning complete.")
