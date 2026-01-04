import argparse
import logging
import sys
from pathlib import Path
from typing import Optional
from PIL import Image, UnidentifiedImageError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def compress_image(
    file_path: Path, 
    output_path: Path, 
    quality: int, 
    resize_factor: int
) -> bool:
    """
    Compress and resize a single image.
    
    Args:
        file_path: Path to the source image.
        output_path: Path where the compressed image will be saved.
        quality: JPEG quality (1-100).
        resize_factor: Factor to divide dimensions by.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        with Image.open(file_path) as image:
            # Calculate new size
            width, height = image.size
            new_size = (width // resize_factor, height // resize_factor)
            
            # Resize
            resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save
            # If the original was PNG/RGBA, saving as JPEG requires conversion
            # We try to preserve the extension, but if the user wants compression,
            # JPEG is usually implied by "quality". However, Pillow handles quality for some other formats too.
            # For safety, if it's RGBA and we are saving to a format that doesn't support it (like JPG), convert.
            if image.mode in ('RGBA', 'P') and output_path.suffix.lower() in ('.jpg', '.jpeg'):
                resized_image = resized_image.convert('RGB')
                
            resized_image.save(output_path, optimize=True, quality=quality)
            logger.info(f"Processed: {file_path.name} -> {output_path}")
            return True
            
    except UnidentifiedImageError:
        # Quietly skip non-image files that might have matched the glob but aren't images
        # or just log as debug/warning
        logger.debug(f"Skipped (Not an image): {file_path}")
        return False
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        return False

def process_directory(
    input_dir: Path, 
    output_dir: Path, 
    quality: int, 
    resize_factor: int, 
    recursive: bool
) -> None:
    """
    Process all images in the directory.
    """
    if not input_dir.exists():
        logger.error(f"Input directory not found: {input_dir}")
        sys.exit(1)

    # Define the pattern for files
    pattern = "**/*" if recursive else "*"
    
    files_processed = 0
    files_skipped = 0

    logger.info(f"Starting compression...")
    logger.info(f"Input: {input_dir}")
    logger.info(f"Output: {output_dir}")
    
    for file_path in input_dir.glob(pattern):
        if file_path.is_file():
            # Determine relative path to maintain structure in output
            try:
                relative_path = file_path.relative_to(input_dir)
            except ValueError:
                # Should not happen with glob from input_dir, but safe guard
                continue
                
            destination_path = output_dir / relative_path
            
            # Basic check to see if it's likely an image before trying to open
            if file_path.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.bmp', '.webp']:
                continue

            success = compress_image(file_path, destination_path, quality, resize_factor)
            if success:
                files_processed += 1
            else:
                files_skipped += 1

    logger.info(f"Completed. Processed: {files_processed}, Skipped/Failed: {files_skipped}")

def main():
    parser = argparse.ArgumentParser(
        description="Batch compress and resize images in a directory."
    )
    
    parser.add_argument(
        "input_dir", 
        type=Path, 
        help="Directory containing images to compress"
    )
    
    parser.add_argument(
        "--output", "-o", 
        type=Path, 
        default=None,
        help="Output directory (default: creates 'compressed_output' next to input)"
    )
    
    parser.add_argument(
        "--quality", "-q", 
        type=int, 
        default=70, 
        help="Image quality (1-100), default: 70"
    )
    
    parser.add_argument(
        "--resize", "-r", 
        type=int, 
        default=2, 
        help="Resize factor (divide dimensions by this number), default: 2"
    )
    
    parser.add_argument(
        "--no-recursive", 
        action="store_true", 
        help="Do not search subdirectories recursively"
    )

    args = parser.parse_args()

    # Setup output directory
    if args.output is None:
        # If input is "pic", output becomes "pic_compressed"
        args.output = args.input_dir.parent / f"{args.input_dir.name}_compressed"
    
    # Validate arguments
    if args.quality < 1 or args.quality > 100:
        logger.error("Quality must be between 1 and 100")
        sys.exit(1)
        
    if args.resize < 1:
        logger.error("Resize factor must be >= 1")
        sys.exit(1)

    process_directory(
        input_dir=args.input_dir,
        output_dir=args.output,
        quality=args.quality,
        resize_factor=args.resize,
        recursive=not args.no_recursive
    )

if __name__ == "__main__":
    main()