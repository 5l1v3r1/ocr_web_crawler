# Import modules
from PIL import Image


def crop_img(filename: str):
    # Open Image file
    img = Image.open(filename)

    # Crop picture files for easier OCR
    box = (105, 77, 370, 125)

    cropped_image = img.crop(box)
    cropped_image.save('Cropper_tmp/temp.png')