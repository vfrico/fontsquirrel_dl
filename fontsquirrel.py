#!/usr/bin/env python3

#   File: fontsquirrel.py
#   Abstract class for downloading fonts from fontsquirrel
#
#   This file is part of fontsquirrel_downloader
#   Pimagizer (C) 2014 Víctor Fernández Rico <vfrico@gmail.com>
#
#   This is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published
#   by the Free Software Foundation, either version 3 of the License,
#   or (at your option) any later version.
#
#   This software is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>
#
# MORE INFO:
#   Api DOCS: <http://www.fontsquirrel.com/blog/2010/12/the-font-squirrel-api>
import json
import shutil
import os
import urllib.request
import logging
import zipfile


logging.basicConfig(level=logging.DEBUG)


class FontSquirrel():
    def get_all_families(self, dest):
        """
        This function allows to user get all families
        availables on FontSquirrel and download them to
        a given folder.
        Returns: Full path of folder containing the fonts
        """
        all_data = self.all_json_data()

        if dest == "":
            dest = "fonts/"
        #print(all_data)
        for font in all_data:
            # For each font listed, get the former name (to save the zip,
            # the url_name (used for api management) and a list of
            # the filenames that should be located on zip
            former_name = font["family_name"]
            url_name = font["family_urlname"]
            font_filename = self.font_family_filenames(url_name)

            download_uri = self.font_download_url(url_name)
            destination = self.download_to(
                download_uri, "tmp/%s.zip" % former_name)

            # Extract all files from zip
            zip_file = zipfile.ZipFile(destination)
            for filename in font_filename:
                logging.debug("Extracting %s font" % filename)
                zip_file.extract(filename, path=dest+url_name)

        return destination

    def get_family(self, familia, destino):
        """
        Given a font family, downloads it from font squirrel to folder
        """
        desired_family = {}

        all_data = self.get_font_list()

        for family in all_data:
            if family['family_url'] == familia:
                desired_family = family
                break

        # Get all files from dictionary "desired_family['files']"
        font_filename = []
        for a in iter(desired_family['files'].items()):
            font_filename.append(a[1])

        logging.debug("Font filenames for family: "+str(font_filename))

        download_uri = self.font_download_url(desired_family['family_url'])

        # Saves the zip
        destination = self.download_to(
            download_uri, "tmp/%s.zip" % desired_family['family'])

        zip_file = zipfile.ZipFile(destination)
        # Extract all files from given zip
        for filename in font_filename:
            zip_file.extract(filename,
                             path=destino+desired_family['family_url'])
        return font_filename

    def get_font_list(self, force_download=False):
        """
        Generates an array of fonts dictionaries. Each dictionary
        has a structure like this:
        {
          'kind': 'fontsquirrel',
          'family': #family_name
          'family_url': #family_urlname
          'category': #Classification
          "variants" : [ "regular" .. "thin" ]
          "files" : {
            "regular" : "http...",
            "thin" : "http...",
          }
        }
        It can be used by others applications to download them or get
        some information about fonts.
        Is similar to Google's font api.
        """
        # return a list of dictionaries with info about fonts: families,
        # styles and how and where to download them
        if force_download:
            logging.info("Force Download is True. Downloading new data")
            all_data = self.all_json_data()
            data_to_return = []
            for family in all_data:
                family_dict = {}
                family_dict["kind"] = "fontsquirrel"
                family_dict["family"] = family["family_name"]
                family_dict["family_url"] = family["family_urlname"]
                family_dict["category"] = family["classification"]

                family_data = self.family_download_json(
                    family["family_urlname"])

                variants = []
                font_files = {}

                for variant in family_data:
                    if variant['style_name'] in font_files:
                        # Not the better solution, but works
                        font_files[str(variant['style_name'])
                                   + "2"] = variant['filename']

                        variants.append(str(variant['style_name']) + "2")

                    else:
                        font_files[variant['style_name']] = variant['filename']
                        variants.append(variant['style_name'])

                family_dict["variants"] = variants
                family_dict["files"] = font_files

                data_to_return.append(family_dict)
                logging.info("Got data from %s family" % family_dict["family"])

            # Save retrieved data to a file
            backup = open('localdata.txt', 'w')
            backup.write(json.dumps(data_to_return))
            backup.close()

            return data_to_return
        else:
            # Open retrieved data
            backup = open('localdata.txt', 'r')
            data = backup.read()
            backup.close()

            a = json.loads(data)
            return a

    def all_json_data(self, force_download=False):
        """
        Retrieves all raw json data from Internet.
        Pending implementation with cache
        """
        url_api = "http://www.fontsquirrel.com/api/fontlist/all"
        request = urllib.request.urlopen(url_api)
        # print ("¿Force Downloading?" + str(force_download))
        return json.loads(request.read().decode('utf-8'))

    def family_download_json(self, family):
        """
        Download json information from internet. It does not
        save any data anywhere.
        """
        request = urllib.request.urlopen(self.family_download_url(family))
        return json.loads(request.read().decode('utf-8'))

    def download_to(self, origin_url, destination_url):
        """
        Helper funtion that downloads a zip file from
        origin url and saves to destination url.
        It doesn't uses urllib.urlretrieve, in order it is
        deprecated on Python 3.X
        Returns: The path of downloaded file.
        """
        logging.info("Downloading zip from %s" % origin_url)
        response = urllib.request.urlopen(origin_url)
        logging.debug("Download finished!")

        try:
            file_out = open(destination_url, 'wb')
        except FileNotFoundError:
            logging.warning("FileNotFoundError exception: \
                  Creating needed folders")
            dirsToCreate = os.path.abspath(destination_url)
            logging.debug("Folder to create:" + str(dirsToCreate))
            os.makedirs(os.path.dirname(dirsToCreate))
            file_out = open(destination_url, 'wb')

        shutil.copyfileobj(response, file_out)
        return destination_url

    def font_family_filenames(self, family):
        """
        Retrieves a list of all filenames of font
        """
        json_data = self.family_download_json(family)

        # number of families
        number = json_data[0]['family_count']

        all_filenames = []

        for font in json_data:
            all_filenames.append(font['filename'])

        return all_filenames

    def font_download_url(self, font_url_name):
        return "http://www.fontsquirrel.com/fonts/download/" + font_url_name

    def family_download_url(self, family):
        return "http://www.fontsquirrel.com/api/familyinfo/" + family

#a = FontSquirrel()
# a.get_font_list()
#a.get_family("roboto", "font/")
#a.get_all_families("")
FontSquirrel().get_all_families("")
