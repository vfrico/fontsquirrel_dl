#!/usr/bin/env python3

# I'll try to retrieve all fonts available freely from fontsquirrel

# Api DOCS: <http://www.fontsquirrel.com/blog/2010/12/the-font-squirrel-api>
import localjson  # Retrieve json data:  localjson.get_json()
import json
import shutil
import os
import urllib.request
import logging
import zipfile


#print (all_data)


def font_download_url(font_url_name):
    return "http://www.fontsquirrel.com/fonts/download/" + font_url_name


def family_download_url(family):
    return "http://www.fontsquirrel.com/api/familyinfo/" + family


def download_to(origin_url, destiny_url):
    logging.info("Downloading zip from %s" % origin_url)
    response = urllib.request.urlopen(origin_url)
    logging.debug("Download finished!")

    try:
        file_out = open(destiny_url, 'wb')
    except FileNotFoundError:
        logging.warning("FileNotFoundError exception: Creating needed folders")
        dirsToCreate = os.path.abspath(destiny_url)
        logging.debug("Folder to create:" + str(dirsToCreate))
        os.makedirs(os.path.dirname(dirsToCreate))
        file_out = open(destiny_url, 'wb')

    shutil.copyfileobj(response, file_out)
    return destiny_url


def font_family_filenames(family):
    "Retrieves a list of all filenames of font"
    request = urllib.request.urlopen(family_download_url(family))
    json_data = json.loads(request.read().decode('utf-8'))
    #print(json_data[0])

    #number of families
    number = json_data[0]['family_count']

    all_filenames = []

    for font in json_data:
        all_filenames.append(font['filename'])

    return all_filenames
font_family_filenames("roboto")

all_data = json.loads(localjson.get_json())
for font in all_data:
    former_name = font["family_name"]
    url_name = font["family_urlname"]
    if int(font["family_count"]) > 1:
        # Need to retrieve more data about this font family
        font_filename = font_family_filenames(url_name)
    else:
        font_filename = [font["font_filename"]]

    download_uri = font_download_url(url_name)
    destiny = download_to(download_uri, "tmp/%s.zip" % former_name)

    print(destiny)

    zip_file = zipfile.ZipFile(destiny)
    print (font_filename)
    for filename in font_filename:
        zip_file.extract(filename,path="fonts/"+url_name)


