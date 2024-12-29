#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os 

os.system('clear')
print ("evening test 3")


import shutil, glob, time, subprocess, re, sys, sqlite3, logging
from datetime import datetime
import datetime as dt
from cloudant.client import Cloudant

import numpy as np
import pandas as pd
import seaborn as sns
from cloudant.query import Query
from cloudant.result import QueryResult
from cloudant.error import ResultException

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.dates as mdates
# from matplotlib import rcParams

import smtplib, ssl,getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


print ("loading imports done")
print ("Building query first...")

USERNAME = "8c1205d4-f169-4cb0-a62e-73d6dba754fb-bluemix"
PASSWORD = "006d4df070101f4d115325956e7f9133a26697c0ab2765c6ed5709f6b26cddbf"


try:
	client = Cloudant(USERNAME,PASSWORD, url = "https://8c1205d4-f169-4cb0-a62e-73d6dba754fb-bluemix:006d4df070101f4d115325956e7f9133a26697c0ab2765c6ed5709f6b26cddbf@8c1205d4-f169-4cb0-a62e-73d6dba754fb-bluemix.cloudantnosqldb.appdomain.cloud" )
	client.connect()
	STATUS1="yes connected!!!!"


except:
	STATUS1="boo...FAILURE"

#print(STATUS1)
my_database = client["temps"]
query = Query(my_database,selector= {'_id': {'$gt': 0}, 'd':dt.datetime.now().strftime("%m-%d-%Y"), 'l':'Backyard'}, fields=['t','temp','d','l'],sort=[{'t': 'desc'}])
temp_dict={}
ALL_temps_dict={}

temp_dict=query(limit=1000, skip=0)['docs']
df = pd.DataFrame(temp_dict)

cur_date=dt.datetime.now().strftime("%m-%d-%Y")

print('query built')
print(df)


















