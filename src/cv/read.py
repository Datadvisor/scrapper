import os
import re
from tqdm import tqdm
from datetime import datetime

import cv2

import pytesseract
from os import path
from matplotlib import pyplot as plt
from cv.filters import filters_dictionary
from pdf2image import convert_from_path

SHOW_FILTERS = False


def find_addresses(content):
    res = []
    find = ["rue", "avenue", "allé", "impasse", "carefour"]
    query = ""

    for idx, elmt in enumerate(find):
        query += '.*' + elmt + '.*'
        if idx != len(find) - 1:
            query += '|'

    addresses = re.findall(query, content)
    for address in addresses:
        res.append(address)
    return res


def find_cities(content):
    res = []
    query = ".*\d{5}.*"

    cities = re.findall(query, content)
    for city in cities:
        res.append(city)
    return res


def find_urls(content):
    res = []
    query = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

    urls = re.findall(query, content)
    for url in urls:
        res.append(url[0])
    return res

def find_emails(content):
    res = []
    query = "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"

    emails = re.findall(query, content)
    for email in emails:
        res.append(email)
    return res

def find_phones(content):
    res = []
    query = "(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}"

    phones = re.findall(query, content)
    for phone in phones:
        res.append(phone)
    return res


def display_res(content, file):
    print("{:<13} {:<64}".format('Key', 'content'))
    file.write("{:<13} {:<64}".format('Key', 'content') + "\n")
    print('----------------------------------------')
    file.write('----------------------------------------' + "\n")
    for k, v in content.items():
        print("{:<13} {:<64}".format(k + ':', len(v)))
        file.write("{:<13} {:<64}".format(k + ':', len(v)) + "\n")
        for idx, elmt in enumerate(v):
            print("{:<13} {:<64}".format(idx, elmt))
            file.write("{:<13} {:<64}".format(idx, elmt) + "\n")
        print('----------------------------------------')
        file.write('----------------------------------------' + "\n")


def open_image(cv_path):
    # Transform the PDF to image to be able to read it
    if path.splitext(cv_path)[1] == '.pdf':
        tmp = convert_from_path(cv_path)[0]
        tmp.save('data/tmp.jpg', 'JPEG')
        img = cv2.imread('data/tmp.jpg')
        os.remove('data/tmp.jpg')
    else:
        img = cv2.imread(cv_path)

    b, g, r = cv2.split(img)
    rgb_img = cv2.merge([r, g, b])
    return rgb_img


def apply_filter(img):
    res = [img]
    show_index = 121

    # Add the original img to the debug display
    if SHOW_FILTERS == True:
        plt.subplot(3, 3, 1), plt.imshow(img), plt.title('original')
        show_index += 1

    # Map over the img to apply all the defined filters
    for idx, (key, function_filter) in enumerate(filters_dictionary.items()):
        start_time = datetime.now()
        filtered = function_filter(img)
        res.append(filtered)
        print("Applying:", key, "in", datetime.now() - start_time)
        if SHOW_FILTERS == True:
            plt.subplot(3, 3, idx + 2), plt.imshow(filtered), plt.title(key)
            show_index += 1

    # Show the debug processed img
    if SHOW_FILTERS == True:
        plt.show()
    return res


def find_personal_info(filtered_list):
    res = {'emails': [], 'cities': [], 'addresses': [], 'phones': [], 'urls': []}

    # Read the CV content
    for filtered in filtered_list:
        cv_content = pytesseract.image_to_string(filtered)
        res['emails'] += find_emails(cv_content)
        res['cities'] += find_cities(cv_content)
        res['addresses'] += find_addresses(cv_content)
        res['phones'] += find_phones(cv_content)
        res['urls'] += find_urls(cv_content)

    # Remove duplicated Element
    for key, content_list in res.items():
        res[key] = list(set(content_list))

    return res


def read_cv(cv_path):
    cvs = []
    final_res = []
    report = open("reports/report_" + datetime.now().strftime("%m-%d-%Y_%H:%M:%S") + ".txt", "w+")

    # Fetch a complete folder
    if os.path.isdir(cv_path):
        for filename in os.listdir(cv_path):
            cvs.append(os.path.join(cv_path, filename))
    else:
        cvs.append(cv_path)

    report.write("-------------------------\n")
    report.write("Numbers of Files: " + str(len(cvs)) + "\n")
    report.write("-------------------------\n")

    for cv in tqdm(cvs):
        print("Looking for:", cv)
        report.write(cv + "\n")
        img = open_image(cv)

        # Apply filters and find information
        filtered_list = apply_filter(img)
        res = find_personal_info(filtered_list)
        final_res.append(res)

        # Display the data
        display_res(res, report)
        report.write("\n\n")
    report.close()
    return final_res

if __name__ == "__main__":
    read_cv('/Users/bricetoffolon/Desktop/AnthoniMarieCV-2023.pdf')