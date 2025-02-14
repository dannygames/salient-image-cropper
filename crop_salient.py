import cv2
import numpy as np
from PIL import Image
import argparse

def crop_salient(image_path, output_path, target_size=1024):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not load image at path: {}".format(image_path))
    h, w, _ = image.shape

    # Calculate adaptive crop size (minimum 1024 or 80% of the smaller dimension)
    crop_size = max(target_size, min(h, w) * 4 // 5)

    # Optional: If the image is smaller than the desired crop size, pad it
    if h < crop_size or w < crop_size:
        top = max((crop_size - h) // 2, 0)
        bottom = crop_size - h - top
        left = max((crop_size - w) // 2, 0)
        right = crop_size - w - left
        image = cv2.copyMakeBorder(image, top, bottom, left, right,
                                   cv2.BORDER_CONSTANT, value=[0, 0, 0])
        h, w, _ = image.shape

    # Compute the saliency map
    saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
    (success, saliencyMap) = saliency.computeSaliency(image)
    if not success:
        raise RuntimeError("Saliency computation failed.")
    
    # Normalize saliency map to [0, 255] and convert to uint8
    saliencyMap = (saliencyMap * 255).astype("uint8")
    
    # Threshold the saliency map to create a binary mask
    _, threshMap = cv2.threshold(saliencyMap, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Compute the center of mass of the salient region
    M = cv2.moments(threshMap)
    if M["m00"] != 0:
        center_x = int(M["m10"] / M["m00"])
        center_y = int(M["m01"] / M["m00"])
    else:
        # Fallback: if no salient region is detected, use image center
        center_x, center_y = w // 2, h // 2

    # Determine crop boundaries ensuring the crop fits within the image
    half_crop = crop_size // 2
    start_x = max(min(center_x - half_crop, w - crop_size), 0)
    start_y = max(min(center_y - half_crop, h - crop_size), 0)

    # Crop the image
    cropped = image[start_y:start_y+crop_size, start_x:start_x+crop_size]
    
    # Resize to target size if necessary
    if crop_size != target_size:
        cropped = cv2.resize(cropped, (target_size, target_size), 
                           interpolation=cv2.INTER_LANCZOS4)

    # Convert from BGR to RGB color space
    cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    
    # Convert to PIL Image and save as WebP
    pil_image = Image.fromarray(cropped_rgb)
    pil_image.save(output_path, 'WEBP', quality=90)
    print("Cropped image saved to:", output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Crop an image to its salient region')
    parser.add_argument('input_path', help='Path to the input image')
    parser.add_argument('output_path', help='Path for the output WebP image')
    parser.add_argument('--size', type=int, default=1024, help='Target size for the output image')
    
    args = parser.parse_args()
    crop_salient(args.input_path, args.output_path, target_size=args.size)
