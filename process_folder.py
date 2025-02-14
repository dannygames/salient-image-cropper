import os
from pathlib import Path
from crop_salient import crop_salient
import argparse

def process_folder(input_folder, target_size=1024):
    """
    Process all JPG images in the input folder and save them as WebP files
    using the crop_salient function.
    
    Args:
        input_folder (str): Path to the folder containing JPG images
        target_size (int): Target size for the cropped images
    """
    # Convert input folder to Path object
    folder_path = Path(input_folder)
    
    # Find all jpg/jpeg files (case insensitive)
    image_files = []
    for ext in ('*.jpg', '*.jpeg', '*.JPG', '*.JPEG'):
        image_files.extend(folder_path.glob(ext))
    
    if not image_files:
        print(f"No JPG images found in {input_folder}")
        return
    
    # Process each image
    for img_path in image_files:
        try:
            # Create output path with .webp extension
            output_path = img_path.with_suffix('.webp')
            
            print(f"Processing: {img_path}")
            crop_salient(str(img_path), str(output_path), target_size)
            print(f"Saved as: {output_path}")
            
        except Exception as e:
            print(f"Error processing {img_path}: {str(e)}")
            continue
            
    print(f"\nProcessing complete. Processed {len(image_files)} images.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a folder of images using crop_salient')
    parser.add_argument('input_folder', help='Path to the folder containing JPG images')
    parser.add_argument('--size', type=int, default=1024, help='Target size for the output images')
    
    args = parser.parse_args()
    process_folder(args.input_folder, args.size) 