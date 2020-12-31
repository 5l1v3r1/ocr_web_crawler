# Import modules
import json
from time import sleep
from random import randint
import requests
from bs4 import BeautifulSoup

from cropper import crop_img
from OCR import img_to_string


def get_letters():
    # Find Letters source
    letters = requests.get('https://iccrc-crcic.ca/find-a-professional-frame/')
    letters_sp = BeautifulSoup(letters.text, 'html.parser')
    # It gets letters list from another source
    letters_src = letters_sp.find('iframe')['src']

    # Send request to the letters source
    letters_list_req = requests.get(letters_src)
    letters_list_sp = BeautifulSoup(letters_list_req.text, 'html.parser')
    letters_list = [letter.contents[0] for letter in letters_list_sp.find_all(
        'a', {'class': 'search_letter'})]

    # Return Letters List
    return letters_list


def get_RCIC_list(letter):
    # Send request to get RCIC list
    RCIC_list_req = requests.post('https://secure.iccrc-crcic.ca/search/do/lang/en',
                                  data={'form_fields': '', 'query': '', 'letter': letter,
                                        'start': 0})
    # Filter JSON to clarify needed info
    RCIC_list_json = json.loads(RCIC_list_req.text)['results']

    # Store filtered json into a list
    RCIC_filtered_list = []
    for result in RCIC_list_json:
        RCIC_dict = {'name': f"{result['step1_surname']}, {result['step1_given_name']}", 'status': result['form_membership_status_text'], 'consultant_id': result['form_consultant_id'],
                     'city': result['city'], 'province': result['state'], 'country': result['country'], 'companies': result['companies'], 'form_id': result['form_id']}
        RCIC_filtered_list.append(RCIC_dict)

    # Return the list
    return RCIC_filtered_list


def get_RCIC_contact_info(form_id):
    # Send request to get contact info
    RCIC_contact_req = requests.get('https://secure.iccrc-crcic.ca/default/search/generate-email-image',
                                    params={'nocache': '', 'lang': 'en', 'form_id': form_id, 'token': ''})

    # Response is in picture file format, so we save it
    RCIC_contact_pic = open('RCIC_contact_pic.png', 'wb')
    RCIC_contact_pic.write(RCIC_contact_req.content)
    RCIC_contact_pic.close()


def main():
    # Get letters list
    letter_list = get_letters()

    # Create a list that contains all of the final filtered info
    RCIC_list_all = []

    for letter in letter_list:
        # Get RCICs list by letters
        RCIC_list = get_RCIC_list(letter)

        # Add email and phone number info to each RCICs list
        for each in RCIC_list:
            # Get contact info image file
            # Adding delay decreases the chance of being caught as a bot
            sleep(randint(1, 3))
            get_RCIC_contact_info(each['form_id'])

            # Crop it for better OCR
            crop_img('RCIC_contact_pic.png')

            # Extract text from contact info picture file
            RCIC_contact_info = img_to_string()

            # Add extracted items to the RCICs list
            each['email'] = RCIC_contact_info['email']
            each['phone_number'] = RCIC_contact_info['phone_number']
            
            each.pop('form_id')  # form_id not needed after getting info

        # Add each RCIC list to the final one
        RCIC_list_all.append(RCIC_list)
    # Save data in a JSON file
    final_json = open('RCIC_list.json', 'a')
    final_json.write(json.dumps(RCIC_list_all, indent=4, sort_keys=True))
    final_json.close()


# Run the application
if __name__ == "__main__":
    print('[ - ] Scraping Started; This may take some time to finish. Until then, grab yourself a coffee and wait :)')
    main()
    print('[ + ] Task has been finished. Data is saved in RCIC_list.json file!')
