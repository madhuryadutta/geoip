import os

from urllib.request import urlretrieve

import zipfile

import mysql.connector
from mysql.connector import Error
import csv

from dotenv import load_dotenv
load_dotenv()

YOUR_LICENSE_KEY=os.getenv('YOUR_LICENSE_KEY')
MaxMind_GeoIP_ZIP_NAME=os.getenv('MaxMind_GeoIP_ZIP_NAME')
Unzipp_Folder='0'

#Connect DB server and database
conn = mysql.connector.connect(
  host = os.getenv('DB_HOST'),
  port = os.getenv('DB_PORT'),
  user = os.getenv('DB_USERNAME'),
  password = os.getenv('DB_PASSWORD'),
  database = os.getenv('DB_DATABASE'),
  ssl_ca = os.getenv('DB_SSL_CA'),
  ssl_verify_cert = os.getenv('DB_SSL_VERIFY_CERT'),
  ssl_verify_identity = os.getenv('DB_SSL_VERIFY_IDENTITY')
)

def func_download_db(filename,LICENSE_KEY):
  url="https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City-CSV&license_key="+YOUR_LICENSE_KEY+"&suffix=zip"
  urlretrieve(url, filename)

def func_unzip_csv(filename,extract_path):
    if os.path.exists(filename):
        with zipfile.ZipFile(filename, 'r') as zip_ref:
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
    if len(dir_list)>=0 :
      Unzipp_Folder=dir_list[0]





# Download CSV Files from maxmind.com official source using own licence key 
filename = "db/"+MaxMind_GeoIP_ZIP_NAME
# func_download_db(filename,YOUR_LICENSE_KEY):

# unziping
# func_unzip_csv(filename,'db/')

# deleting zip file 
# func_zip_delete(filename):

func_find_extract_folder_name()

print(Unzipp_Folder)







cursor = conn.cursor()

cursor.execute('''create table IF NOT EXISTS ipv4
(
    id                             int NOT NULL AUTO_INCREMENT,
    network                        varchar(255),
    geoname_id                     varchar(255),
    registered_country_geoname_id  varchar(255),
    represented_country_geoname_id varchar(255),
    is_anonymous_proxy             varchar(255),
    is_satellite_provider          varchar(255),
    postal_code                    varchar(255),
    latitude                       varchar(255),
    longitude                      varchar(255),
    accuracy_radius                varchar(255),
    PRIMARY KEY (id)
)''')

ipv4_file=Unzipp_Folder+"/GeoLite2-City-Blocks-IPv4.csv"
#open the csv file
with open(ipv4_file, mode='r') as csv_file:
    #read csv using reader class
    csv_reader = csv.reader(csv_file)
    #skip header
    header = next(csv_reader)
    #Read csv row wise and insert into table
    for row in csv_reader:
        sql = "INSERT INTO users (name, mobile, email) VALUES (%s,%s,%s)"
        cursor.execute(sql, tuple(row))
        print("Record inserted")

conn.commit()
cursor.close()