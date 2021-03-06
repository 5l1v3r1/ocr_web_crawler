# OCR Web Crawler
A web crawler for getting all of RCIC lists and converting their contact card images to text from "https://iccrc-crcic.ca/find-a-professional-frame" website.

## What is the website?
* The website mentioned above contains a list of RCICs (Regulated Canadian Immigration Consultants) with different information such as their name, companies, consultant identifications, etc.
* The list of RCICs are filtered by letters, so you should click on each letter to get different lists of RCICs. 
* Each element in the list has a contact button. When you press it, a js popup window will appear that gets the contact info from again, ANOTHER source!
* The popup window yet has another contact button that when clicked, will preview an image containing other contact information such as email and phone number.

## What does my crawler do about it?
<b> It gets each RCIC's name, consultant id, companies list, email, phone number, country, province, city, etc. and does some operations on them; then it writes them into JSON file.</b>

## That's how it works:
* It first gets all of the letters list from the identified source. I could generate them manually (letters, no big deal!), but I wanted my app to work dynamically and get the info that are actually NEEDED.
* After that, It will send request to an endpoint containing the letter. The endpoint will return a JSON response containing more than 500 items for EACH LETTER!
* So what it does here, is to filter the results for each letter, get only the items that we need, and add them to a list; because the given JSON response has so 2x more items that we don't even need.
* The endpoint that gives us RCIC lists based on letters, doesn't contain email and phone number. Instead, we should send request to another endpoint to get an image file containing those info.
* The downloaded picture has 480 x 125 size, containing 6 rows of texts. Tesseract (As our OCR engine) can't extract texts we need, because the image is like a captcha image.
* Only 2 rows actually contained the info that we couldn't get from previous endpoint. So I created a cropper.py file that gets a filename and then crops it in a way that only two final rows are visible. This way, it's easier for tesseract to extract info from it.
* Ok, to get out of these image scraping stuff, let's get back to our web scraping! After extracting the needed info from the image file, the program adds them to the list (As you can imagine, all of these operations related to downloading and processing images are just done for one RCIC out of more than 500 RCICs and for one RCIC list out of 26 lists!)
* Finally, we write the prettified and filtered JSON data to a file named "RCIC_list.json". There is an example in the github repo for it.

* <b>All of these operations took exactly 59 min. to finish on my pc (considering that it is a potato one and we have a large amount of data being processed). </b>
