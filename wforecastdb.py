#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function

import datetime
import os
import sys
import time
import requests
import json
import ast
import smtplib
import schedule
import mysql.connector
from string import Template
from datetime import datetime
from datetime import timedelta
from datetime import date

def read_template(filename):
    with open(filename, 'r') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)
    
#print( "Connecting to mysql database")

# some string constants
SINGLE_HASH = "#"
HASHES = "########################################"
SLASH_N = "\n"

#connect to the database. Enter your host, username and password
#cnx = mysql.connector.connect(user='user', password='password', host='host', database='database')
#cursor = cnx.cursor()

def main():
    if True:
       print(HASHES)
       #connect to the database. Enter your host, username and password
       print("Connecting to MySQL database")
       cnx = mysql.connector.connect(user='user', password='password', host='host', database='database')
       cursor = cnx.cursor()    
       print("Downloading daily data from Weather Underground")
       today = date.today()
       url = requests.get('https://api.weather.com/v2/pws/dailysummary/7day?stationId={stationID}&format=json&units=m&apiKey={APIKEY}&numericPrecision=decimal')
       json_d = json.loads(url.text)
       obs = format(json.dumps(json_d))
       a = json.loads(obs)
       b = a['summaries']
       c = format(json.dumps(b))
       d = json.loads(c)
       e = d[5]
       f = e['metric']
       g = format(json.dumps(f))
       h = json.loads(g)
       v = h
       insert_Gauged = "INSERT INTO Gauged(validTimeLocal,temperatureMax,temperatureMin,precipTotal) VALUES (%s, %s, %s, %s)"
       print("Downloading forecast data from Weather Underground")
       url4cast = requests.get('https://api.weather.com/v3/wx/forecast/daily/5day?geocode={lat},{lon}&format=json&units=m&language=sp-SPAIN&apiKey={APIKEY}')
       json_data = json.loads(url4cast.text)
       observe = format(json.dumps(json_data))
       insert_Forecast0 = "INSERT INTO Forecast0(validTimeLocal,temperatureMax,temperatureMin,precipTotal) VALUES (%s, %s, %s, %s)"
       insert_Forecast1 = "INSERT INTO Forecast1(validTimeLocal,temperatureMax,temperatureMin,precipTotal) VALUES (%s, %s, %s, %s)"
       insert_Forecast2 = "INSERT INTO Forecast2(validTimeLocal,temperatureMax,temperatureMin,precipTotal) VALUES (%s, %s, %s, %s)"
       insert_Forecast3 = "INSERT INTO Forecast3(validTimeLocal,temperatureMax,temperatureMin,precipTotal) VALUES (%s, %s, %s, %s)"
       insert_Forecast4 = "INSERT INTO Forecast4(validTimeLocal,temperatureMax,temperatureMin,precipTotal) VALUES (%s, %s, %s, %s)"
       y = json.loads(observe)
       j_1 = date.today()-timedelta(days=1)
       j0 = date.today()
       j1 = date.today()+timedelta(days=1)
       j2 = date.today()+timedelta(days=2)
       j3 = date.today()+timedelta(days=3)
       j4 = date.today()+timedelta(days=4)       
       k = y['temperatureMax']
       l = y['temperatureMin']
       m = y['qpf']
       print('Recording values in Data Bases')
       val = (j_1, v['tempHigh'], v['tempLow'], v['precipTotal'])
       val0 = (j0, k[0], l[0], m[0])
       val1 = (j1, k[1], l[1], m[1])
       val2 = (j2, k[2], l[2], m[2])
       val3 = (j3, k[3], l[3], m[3])
       val4 = (j4, k[4], l[4], m[4])
       cursor.execute(insert_Gauged, val)
       cursor.execute(insert_Forecast0, val0)
       cursor.execute(insert_Forecast1, val1)
       cursor.execute(insert_Forecast2, val2)
       cursor.execute(insert_Forecast3, val3)
       cursor.execute(insert_Forecast4, val4)
       cnx.commit()
 
       print(today.strftime("%d/%m/%Y"),'-> Values written into Data Bases')

# ============================================================================
# here's where we start doing stuff
# ============================================================================
print(SLASH_N + HASHES)
print(SINGLE_HASH, "Forecast QA from WU      ", SINGLE_HASH)
print(SINGLE_HASH, "By Pablo Blanco-Gomez    ", SINGLE_HASH)
print(HASHES)

# Now see what we're supposed to do next
if __name__ == "__main__":
   schedule.every().day.at("08:05").do(main)
   while True:
       schedule.run_pending()
       time.sleep(1)
