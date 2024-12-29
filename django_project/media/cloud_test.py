#!/usr/bin/python
# -*- coding:UTF-8 -*-


#git update 1/27/2021
import cloudant
from cloudant.client import Cloudant
import os


from datetime import datetime
import datetime as dt
# import os, shutil, glob, time, subprocess, re, sys, sqlite3, logging, smtplib
# import RPi.GPIO as GPIO
# from datetime import timedelta

# import wiotp.sdk.application
# from cloudant.client import Cloudant
# from cloudant.query import Query
# from cloudant.result import QueryResult
# from cloudant.error import ResultException

#	client = Cloudant(user_data['cloud_acct_username'],user_data['cloud_acct_pword'], url = user_data['cloud_act_url'] )


def get_user_data():
	user_data = {}
	with open("new_user_data.txt") as f:
		for line in f:
			(field, val) = line.split()
			user_data[field] = val

	# print ("cloudant account URL = ", user_data['cloud_act_url'])
	# print ("cloudant account API key = ", user_data['cloud_acct_API_key'])
	# print ("gmail user account name = ",user_data['gmail_user'])
	# print ("gmail user password = ",user_data['gmail_password'])
	# print ("cloudant username = ",user_data['cloud_acct_username'])
	# print ("cloudant top level name = ",user_data['cloud_top_level_account_username'])
	return user_data




os.system('clear')
print ("cloud test")
print("\n")
get_user_data()
print("\n")
print("testing cloud connection....")
print("\n")
user_data=get_user_data()

#client = Cloudant(user_data['cloud_acct_username'],user_data['cloud_acct_pword'], url = user_data['cloud_act_url'] )
# client = Cloudant.iam(user_data['cloud_acct_username'], user_data['cloud_acct_API_key'], connect=True)

client = Cloudant.iam(None, user_data['cloud_acct_API_key'], url='https://59bbdd02-d61b-4875-af81-9934d7e21be1-bluemix.cloudantnosqldb.appdomain.cloud', connect=True)



# client.connect()
print ("connected")
DATABASE_NAME="hms_log"

my_database = client[DATABASE_NAME]
msg="test message"

json_document = {
     "c":"INFO",
     "d": "test date",
     "t":dt.datetime.now().strftime("%H:%M:%S"),
     "m":msg
}

try:
	new_document = my_database.create_document(json_document)
except:
	print ('error writing to database')
	time.sleep(30)
	try:
		new_document = my_database.create_document(json_document)
	except:
		print('fail')
		pass
client.disconnect()









