#!/usr/bin/env python3

# I'll try to retrieve all fonts available freely from fontsquirrel

# Api DOCS: <http://www.fontsquirrel.com/blog/2010/12/the-font-squirrel-api>
# import localjson  # Retrieve json data:  localjson.get_json()
import json
import shutil
import os
import urllib.request
import logging
import zipfile


logging.basicConfig(level=logging.DEBUG)


class FontSquirrel():
    def get_all_families(self, destination):
        # Given a folder, download to it all font squirrel fonts available
        all_data = self.all_json_data()

        if destination == "":
            destination = "fonts/"

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

            print(destination)

            zip_file = zipfile.ZipFile(destination)
            print(font_filename)
            for filename in font_filename:
                zip_file.extract(filename, path=destination+url_name)

    def get_family(self,familia, destino):
        # Given a font family, downloads from font squirrel to folder
        desired_family = {}

        all_data = self.get_font_list(force_download=True)
        print("\n\n\n\n")
        print(all_data)
        print("\n\n\n\n")
        for family in all_data:
            if family['family_url'] == familia:
                desired_family = family
                break;

        font_filename = []
        for a in iter(desired_family['files'].items()):
            print(a)
            font_filename.append(a[1])
        print(font_filename)

        download_uri = self.font_download_url(desired_family['family_url'])
        destination = self.download_to(
            download_uri, "tmp/%s.zip" % desired_family['family'])

        print(destination)

        zip_file = zipfile.ZipFile(destination)
        print(font_filename)
        for filename in font_filename:
            zip_file.extract(filename, path=destino+desired_family['family_url'])

    def get_font_list(self,force_download=False):
        """
        {
          'kind': 'fontsquirrel',
          'family': #family_name
          'family_url': #family_urlname
          'category': #Classification
          "variants" : [ "regular" .. "thin" ]
          "files" : [
          "regular" : "http...",
          "thin" : "http...",
          ]
        }
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

                family_data = self.family_download_json(family["family_urlname"])

                variants =  []
                font_files = {}

                for variant in family_data:

                    if variant['style_name'] in font_files :
                        font_files[str(variant['style_name']) + "2"] = variant['filename']
                        variants.append(str(variant['style_name']) + "2")
                    else:
                        font_files[variant['style_name']] = variant['filename']
                        variants.append(variant['style_name'])

                family_dict["variants"] = variants
                family_dict["files"] = font_files

                data_to_return.append(family_dict)
                logging.info("Retrieved data from %s family" % family_dict["family"])

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

    def all_json_data(self, force_download = False):
        url_api = "http://www.fontsquirrel.com/api/fontlist/all"
        request = urllib.request.urlopen(url_api)
        # print ("¿Force Downloading?" + str(force_download))
        return json.loads(request.read().decode('utf-8'))

    def download_to(self, origin_url, destination_url):
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
        "Retrieves a list of all filenames of font"
        json_data = self.family_download_json(family)
        # print(json_data[0])

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

    def family_download_json(self, family):
        request = urllib.request.urlopen(self.family_download_url(family))
        return json.loads(request.read().decode('utf-8'))

a = FontSquirrel()
#a.get_font_list()
a.get_family("roboto","font/")
#a.get_all_families("")
