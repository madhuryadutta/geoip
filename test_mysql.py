import os
import mysql.connector
from mysql.connector import Error
import csv
from dotenv import load_dotenv
load_dotenv()
#Connect DB server and database
conn = mysql.connector.connect(
  host = os.getenv('DB_HOST'),
  port = os.getenv('DB_PORT'),
  user = os.getenv('DB_USERNAME'),
  password = os.getenv('DB_PASSWORD'),
  database = os.getenv('DB_DATABASE'),
  ssl_ca = os.getenv('DB_SSL_CA'),
  ssl_verify_cert = True,
  ssl_verify_identity = True
)


cursor = conn.cursor()

cursor.execute('''create table IF NOT EXISTS users
(
    id     int NOT NULL AUTO_INCREMENT,
    name   varchar(255),
    mobile varchar(255),
    email  varchar(255),
    PRIMARY KEY (id)
)''')

#open the csv file
with open('users.csv', mode='r') as csv_file:
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
