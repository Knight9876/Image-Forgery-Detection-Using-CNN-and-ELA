import os, sys
import numpy as np
from PIL import Image, ImageChops, ImageEnhance, ImageDraw

# converts input image to ela applied image
def convert_to_ela_image(path, quality):

    original_image = Image.open(path).convert("RGB")

    # resaving input image at the desired quality
    resaved_file_name = "results/resaved_image.jpg"  # predefined filename for resaved image
    original_image.save(resaved_file_name, "JPEG", quality=quality)
    resaved_image = Image.open(resaved_file_name)

    # pixel difference between original and resaved image
    ela_image = ImageChops.difference(original_image, resaved_image)

    # scaling factors are calculated from pixel extremas
    extrema = ela_image.getextrema()
    max_difference = max([pix[1] for pix in extrema])
    if max_difference == 0:
        max_difference = 1
    scale = 350.0 / max_difference

    # enhancing elaimage to brighten the pixels
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

    ela_image.save("ela_image.png")
    return ela_image

def convert_to_ela_image_gray(path, quality):
    original_image = Image.open(path).convert("RGB")
    ela_image = convert_to_ela_image(path, quality)
    ela_image_gray = ela_image.convert("L")
    return original_image, ela_image_gray

def adaptive_threshold(ela_image_gray):
    # Convert grayscale ELA image to a numpy array
    ela_array = np.array(ela_image_gray)

    # Calculate mean and standard deviation
    mean = np.mean(ela_array)
    std_dev = np.std(ela_array)

    # Set threshold as mean + standard deviation
    threshold = mean + std_dev

    return threshold

def dynamic_thresholding(image, block_size=15, c=10):
    """
    Applies adaptive thresholding to an image.
    
    :param image: Grayscale PIL image
    :param block_size: Size of the neighborhood region
    :param c: Constant to subtract from the mean or weighted sum
    :return: Binary image (PIL Image)
    """
    image = image.convert('L')
    arr = np.array(image)

    # Apply adaptive mean thresholding
    thresholded = np.zeros_like(arr)
    
    for i in range(0, arr.shape[0], block_size):
        for j in range(0, arr.shape[1], block_size):
            block = arr[i:i+block_size, j:j+block_size]
            mean = np.mean(block)
            thresholded[i:i+block_size, j:j+block_size] = block > (mean - c)
    
    return Image.fromarray(thresholded * 255).convert('RGB')

def highlight_forged_areas(original_image, ela_image_gray):
    threshold = adaptive_threshold(ela_image_gray)
    original = original_image.copy()

    for y in range(original.height):
        for x in range(original.width):
            pixel_value = ela_image_gray.getpixel((x, y))
            if pixel_value > threshold:
                # Overwrite pixel with red
                original.putpixel((x, y), (255, 0, 0))

    output_path = "results/processed_image.png"
    original.save(output_path)
    return output_path

if __name__ == "__main__":
    file_path = sys.argv[1]
    quality = int(sys.argv[2])
    convert_to_ela_image(file_path, quality).show()
