#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
#   File: fontsquirrel.py
#   Abstract class for downloading fonts from fontsquirrel
#
#   This file is part of fontsquirrel_downloader
#   Pimagizer (C) 2014-2016 Víctor Fernández Rico <vfrico@gmail.com>
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
#   Api DOCS:
#     <http://www.fontsquirrel.com/blog/2010/12/the-font-squirrel-api>
"""Abstract class for downloading fonts from fontsquirrel."""

import json
import shutil
import os
import urllib.request
import logging
import zipfile
# import threading
import multiprocessing


class FoldersToSave():
    """Utility class to get standard folder destinations."""
    # Home directory of user
    userfolder = os.path.expanduser("~")

    def getFontSquirrel(self):
        return os.path.join(self.cache(file_cache='fontsquirrel'), "data.json")

    def join_path_with_home(self, path_to_join):
        """Returns folder and creates recursively
        the directory on filesystem"""
        directory = os.path.join(self.userfolder, path_to_join)

        # Creates recursively directory. Last argument prevents OSError
        os.makedirs(directory, exist_ok=True)
        return directory

    def cache(self, file_cache=None):
        """Default dir to save font cache"""
        if file_cache is None:
            return self.join_path_with_home(".config/FontSquirrel_dl/cache")
        else:
            return self.join_path_with_home(
                ".config/FontSquirrel_dl/cache/"+file_cache)

    def font(self):
        """Default dir to save downloaded fonts"""
        return self.join_path_with_home(".fonts/FontSquirrel/")

    def tmp(self):
        """Default dir to use temporally"""
        return self.join_path_with_home(".config/FontSquirrel_dl/tmp")


logging.basicConfig(level=logging.INFO)


class FontSquirrel():
    """Abstract class for downloading fonts from fontsquirrel."""

    def __init__(self):
        pass

    def __download_info_family__(self, family):
        print ("hoola estoy descargando!!")
        family_dict = dict()
        family_dict["kind"] = "fontsquirrel"
        family_dict["family"] = family["family_name"]
        family_dict["family_url"] = family["family_urlname"]
        family_dict["category"] = family["classification"]
        family_data = self.family_download_json(family["family_urlname"])

        variants = []
        font_files = {}

        for variant in family_data:
            if variant['style_name'] in font_files:
                # Not the best solution, but works
                font_files[str(variant['style_name']) +
                           "2"] = variant['filename']

                variants.append(str(variant['style_name']) + "2")

            else:
                font_files[variant['style_name']] = variant['filename']
                variants.append(variant['style_name'])

        family_dict["variants"] = variants
        family_dict["files"] = font_files

        logging.info("Got data from %s family" % family_dict["family"])
        return family_dict

    def get_font_list(self, force_download=True, use_threads=True):
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
            logging.info("Downloading new data")
            all_data = self.all_json_data()
            data_to_return = []
            # print(multiprocessing.cpu_count()*10)
            with multiprocessing.Pool(multiprocessing.cpu_count()*5) as p:
                data_to_return = p.map(self.__download_info_family__, all_data)

            backup = open(FoldersToSave().getFontSquirrel(), 'w')
            backup.write(json.dumps(data_to_return))
            backup.close()

            return data_to_return
        else:
            # Open retrieved data
            dictionary = {}
            try:
                backup = open(FoldersToSave().getFontSquirrel(), 'r')
                data = backup.read()
                backup.close()
                dictionary = json.loads(data)

            except FileNotFoundError:
                logging.info("Couldn't locate localdata.txt. Forcing download")
                self.get_font_list(force_download=True)

            return dictionary

    @staticmethod
    def all_json_data(force_download=False):
        """
        Retrieves all raw json data from Internet.
        Pending implementation with cache
        """
        url_api = "http://www.fontsquirrel.com/api/fontlist/all"
        request = urllib.request.urlopen(url_api)
        print("¿Force Downloading?" + str(force_download))
        return json.loads(request.read().decode('utf-8'))

    def get_all_families(self, dest):
        """
        Given a parameter "dest" (must be a directory), downloads all
        fonts available on FontSquirrel to folder "dest".

        Returns: Full path of folder containing the fonts
        """
        all_data = self.all_json_data()
        destination = None
        if dest == "":
            dest = "fonts/"

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

        all_data = self.get_font_list(force_download=False)

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

        destino = os.path.abspath(
            os.path.expanduser(destino + desired_family['family_url']))
        zip_file = zipfile.ZipFile(destination)
        # Extract all files from given zip
        for filename in font_filename:
            zip_file.extract(filename,
                             path=destino)
        return font_filename

    def family_download_json(self, family):
        """
        Download json information from internet. It does not
        save any data anywhere.
        """
        request = urllib.request.urlopen(self.family_download_url(family))
        return json.loads(request.read().decode('utf-8'))

    @staticmethod
    def download_to(origin_url, destination_url):
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
            dirs_to_create = os.path.abspath(destination_url)
            logging.debug("Folder to create:" + str(dirs_to_create))
            os.makedirs(os.path.dirname(dirs_to_create))
            file_out = open(destination_url, 'wb')

        shutil.copyfileobj(response, file_out)
        file_out.close()
        return destination_url

    def font_family_filenames(self, family):
        """
        Given a parameter "family", returns a list with the file names
        which are part of the font.
        """
        json_data = self.family_download_json(family)

        # number of families
        # number = json_data[0]['family_count']

        all_filenames = []

        for font in json_data:
            all_filenames.append(font['filename'])

        return all_filenames

    @staticmethod
    def font_download_url(font_url_name):
        return "http://www.fontsquirrel.com/fonts/download/" + font_url_name

    @staticmethod
    def family_download_url(family):
        return "http://www.fontsquirrel.com/api/familyinfo/" + family
