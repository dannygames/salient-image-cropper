# Salient Image Cropper

A Python tool that automatically crops images to their most visually significant regions using saliency detection. The cropped images are saved in WebP format for optimal quality and file size.

## Features

- Automatically detects and crops to the most visually important part of an image
- Maintains minimum dimensions to preserve image quality
- Supports batch processing of multiple images
- Converts images to space-efficient WebP format
- Handles images of varying sizes
- Falls back to center cropping if no salient region is detected

## Requirements

Install the necessary Python packages with:

```bash
pip install opencv-python numpy Pillow
```

## Usage

### Single Image Processing

Process a single image using the `crop_salient.py` script:

```bash
python crop_salient.py input_image.jpg output_image.webp [--size SIZE]
```

Arguments:
- `input_image.jpg`: Path to the input image
- `output_image.webp`: Path for the output WebP image
- `--size`: Target size for the output image (default: 1024)

### Batch Processing

Process an entire folder of images using the `process_folder.py` script:

```bash
python process_folder.py input_folder [--size SIZE]
```

Arguments:
- `input_folder`: Path to the folder containing JPG images
- `--size`: Target size for all output images (default: 1024)

The script will:
1. Find all JPG/JPEG files in the input folder
2. Process each image using the salient region detection
3. Save the cropped images as WebP files in the same folder

## How It Works

1. The tool loads the input image and calculates an appropriate crop size
2. It computes a saliency map using OpenCV's Spectral Residual method
3. The center of mass of the salient region is determined
4. The image is cropped around this center point
5. The result is saved as a WebP file with high quality settings

## Error Handling

- Gracefully handles images that can't be loaded
- Falls back to center cropping if saliency detection fails
- Continues processing remaining images if one fails in batch mode
- Provides informative error messages

## Notes

- Input images can be any size - smaller images will be padded if necessary
- Output images are always square with dimensions specified by `--size`
- Supported input formats: JPG, JPEG (case insensitive)
- Output format: WebP (90% quality)