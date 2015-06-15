#!/usr/bin/env python3
fi = open('googledata.json','r')
jsonfile = fi.read()
import json, os
import urllib.request
import shutil

#String used to delete the previous line on "download"
blstring = ""
for i in range(0,79):
    blstring += " "

class GoogleFont():
    number_downloaded = 0

    def get_updated_json(self):
        url = "https://www.googleapis.com/webfonts/v1/webfonts?key=AIzaSyBDjNcwLIS77aqQstOdqrFDobzuihtwRVI"
        response = urllib.request.urlopen(url)
        dest = "./localdata.json"
        try:
            file_out = open(dest, 'wb')
        except FileNotFoundError:
            dirs_to_create = os.path.abspath(dest)
            os.makedirs(os.path.dirname(dirs_to_create))
            file_out = open(dest, 'wb')

        shutil.copyfileobj(response, file_out)
        return dest

    def extract_data_from_json(self,jsonfile):
        directories = []
        files = []
        itemsFont = json.loads(jsonfile)['items']
        for family in itemsFont:
            family_name = family['family'].replace(' ', '-').lower()
            directories.append(family_name)
            for file in family['files']:
                ext = family['files'][file].split('.')[-1]
                font = ["/"+family_name+"/"+family_name+"-"+file+"."+ext,
                    family['files'][file]]
                files.append(font)
        return files


    def download_families(self,files,parent_directory):
        for file in files:
            dest = parent_directory+file[0]
            response = urllib.request.urlopen(file[1])
            try:
                file_out = open(dest, 'wb')
            except FileNotFoundError:
                dirs_to_create = os.path.abspath(dest)
                os.makedirs(os.path.dirname(dirs_to_create))
                file_out = open(dest, 'wb')

            shutil.copyfileobj(response, file_out)

            self.number_downloaded += 1
            pc = self.number_downloaded / len(files) * 100
            print(blstring,end="\r")
            print("Downloading {1} of {2} ... {3:.1f}%. File: {0}...".format(file[0][:36],self.number_downloaded,len(files),pc),end="\r")
        print ("\nDone")

    def download_all(self,dest):
        file = self.get_updated_json()
        fi = open(file,'r')
        jsonfile = fi.read()
        fontfiles = self.extract_data_from_json(jsonfile)
        self.download_families(fontfiles,dest)

a = GoogleFont()
a.download_all("gogfont")
