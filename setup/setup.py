import os

from urllib.request import urlretrieve

import zipfile

import csv

YOUR_LICENSE_KEY = os.getenv("YOUR_LICENSE_KEY")
MaxMind_GeoIP_ZIP_NAME = os.getenv("MaxMind_GeoIP_ZIP_NAME")
Unzipp_Folder = "0"


def func_download_db(filename, LICENSE_KEY):
    url = (
        "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City-CSV&license_key="
        + YOUR_LICENSE_KEY
        + "&suffix=zip"
    )
    urlretrieve(url, filename)


def func_unzip_csv(filename, extract_path):
    if os.path.exists(filename):
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(extract_path)
            print("unzip completed")
    else:
        print("The file does not exist")


def func_zip_delete(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print("The file does not exist")


def func_find_extract_folder_name():
    global Unzipp_Folder
    path = "./db"
    dir_list = os.listdir(path)
    dir_list.sort()
    if len(dir_list) >= 0:
        Unzipp_Folder = dir_list[0]


# Download CSV Files from maxmind.com official source using own licence key
filename = "db/" + MaxMind_GeoIP_ZIP_NAME
# func_download_db(filename,YOUR_LICENSE_KEY)

# unziping
func_unzip_csv(filename, "db/")

# deleting zip file
func_zip_delete(filename)

func_find_extract_folder_name()

print(Unzipp_Folder)
