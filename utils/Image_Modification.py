import cv2
import numpy as np
import os
from PIL import Image

def remove_background(object_image_path, background_image_path):
    """
    Remove background from the object image using color-based masking.

    Parameters:
    - object_image_path: Path to the image with the object.
    - background_image_path: Path to the image without the object.

    Returns:
    - The result image after placing the object on a new background.
    """

    # Read the images
    object_image = cv2.imread(object_image_path)
    background_image = cv2.imread(background_image_path)

    # Check if images were loaded properly
    if object_image is None or background_image is None:
        raise ValueError("One or both of the image paths are incorrect or the images could not be loaded.")

    # Resize background image to match object image size
    background_image = cv2.resize(background_image, (object_image.shape[1], object_image.shape[0]))

    # Convert images to grayscale
    gray_object = cv2.cvtColor(object_image, cv2.COLOR_BGR2GRAY)
    gray_background = cv2.cvtColor(background_image, cv2.COLOR_BGR2GRAY)

    # Perform background subtraction
    diff_image = cv2.absdiff(gray_object, gray_background)

    # Apply a Gaussian blur to reduce noise
    blurred_diff = cv2.GaussianBlur(diff_image, (5, 5), 0)

    # Threshold to create a binary mask of the object
    _, mask = cv2.threshold(blurred_diff, 30, 255, cv2.THRESH_BINARY)

    # Refine mask using morphological operations (to remove noise)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Convert the mask to 3 channels to match the object image
    mask_3ch = cv2.merge([mask, mask, mask])

    # Extract the object from the object image using the mask
    object_extracted = cv2.bitwise_and(object_image, mask_3ch)

    # Convert extracted image to RGBA (with alpha channel)
    b, g, r = cv2.split(object_extracted)
    rgba = [b, g, r, mask]  # Use mask as the alpha channel
    object_with_alpha = cv2.merge(rgba, 4)

    return object_with_alpha



def place_on_new_background(object_image_path, new_background_path):
    """
    Place the extracted object on a new background.

    Parameters:
    - object_image_path: Path to the extracted object image.
    - new_background_path: Path to the desired new background image.
    - session_data: Dictionary containing session-related information.

    Returns:
    - The final composite image path.
    """

    # Open the images
    object_image = Image.open(object_image_path).convert("RGBA")
    new_background = Image.open(new_background_path).convert("RGBA")

    # Resize the background to match the object image
    new_background = new_background.resize(object_image.size)

    # Composite the object onto the new background
    composite_image = Image.alpha_composite(new_background, object_image)

    # Convert the image to RGB before saving
    composite_image = composite_image.convert("RGB")

    # Save the final composite image
    # final_image_path = os.path.join(session_data["session_dir"], 'RPI_Final.jpg')
    # composite_image.save(final_image_path)

    return composite_image

# Test module
if __name__ == '__main__':

    #Extract the object first
    object_image_path = os.path.join(os.path.dirname( __file__ ), '..', 'Background_modification', 'Background_with_object.jpg')
    background_image_path = os.path.join(os.path.dirname( __file__ ), '..', 'Background_modification', 'Background.jpg')

    extracted_result = remove_background(object_image_path, background_image_path)
    save_path = os.path.join(os.path.dirname( __file__ ), '..', 'Background_modification', 'Extracted_object', 'extracted_result.png')

    #Save the image with extracted object
    cv2.imwrite(save_path, extracted_result)

    #Add new background
    extracted_image_path = save_path #The result from the remove_background() is the extracted object image
    new_background_path = os.path.join(os.path.dirname( __file__ ), '..', 'Background_modification', 'black_background.png')

    final_image = place_on_new_background(extracted_image_path, new_background_path)
    final_image_path = os.path.join(os.path.dirname( __file__ ), '..', 'Background_modification', 'Final_result', 'FinalImg_result.png')
    final_image.save(final_image_path)



