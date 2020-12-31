# Import modules
import pytesseract
from config import Config
import os

# Configure pytesseract
pytesseract.pytesseract.tesseract_cmd = (rf"{Config.TESSERACT_CMD_PATH}")


def img_to_string():
    # Extract text from picture
    pic_str = pytesseract.image_to_string(r"Cropper_tmp/temp.png")

    #Return a dictionary containing the extracted info
    pic_str_list = pic_str.split("\n")
    try:
        contact_info = {"email": pic_str_list[0], "phone_number": pic_str_list[1]}
    except IndexError: # Handle the situation if the image does not contain the needed data
        try:
            if type(pic_str_list[0]) == int:
                contact_info = {"email": "", "phone_number": pic_str_list[0]}
            elif type(pic_str_list[0]) == str:
                contact_info = {"email": pic_str_list[0], "phone_number": ""}
            elif pic_str_list[0] == '\f':
                contact_info = {"email": "", "phone_number": ""}
        except IndexError:
            contact_info = {"email": "", "phone_number": ""}
    return contact_info
