#!/usr/bin/python
# -*- coding:UTF-8 -*-




from cloudant.client import Cloudant
from datetime import datetime
import datetime as dt
from cloudant.query import Query
from cloudant.result import QueryResult

print("test one")

USERNAME = "8c1205d4-f169-4cb0-a62e-73d6dba754fb-bluemix"
PASSWORD = "006d4df070101f4d115325956e7f9133a26697c0ab2765c6ed5709f6b26cddbf"


try:
  client = Cloudant(USERNAME,PASSWORD, url = "https://8c1205d4-f169-4cb0-a62e-73d6dba754fb-bluemix:006d4df070101f4d115325956e7f9133a26697c0ab2765c6ed5709f6b26cddbf@8c1205d4-f169-4cb0-a62e-73d6dba754fb-bluemix.cloudantnosqldb.appdomain.cloud" )
  client.connect()
  STATUS1="yes connected!!!!"


except:
  STATUS1="boo...FAILURE"

print(STATUS1)

my_database = client["temps"]
query = Query(my_database,selector= {'_id': {'$gt': 0}, 'd':dt.datetime.now().strftime("%m-%d-%Y"), 'l':'Backyard'}, fields=['t','temp','d','l'],sort=[{'t': 'desc'}])
temp_dict={}

temp_dict=query(limit=10, skip=0)['docs']
#df = pd.DataFrame(temp_dict)
cur_date=dt.datetime.now().strftime("%m-%d-%Y")

TEMP_DICT=temp_dict
print('the length of readings=', len (temp_dict))

#print (TEMP_DICT)
print ('\n')
for row in TEMP_DICT:
	print ('in the', row['l'], 'on', row['d'],'at', row['t'], 'the temperature was:',row['temp'])
