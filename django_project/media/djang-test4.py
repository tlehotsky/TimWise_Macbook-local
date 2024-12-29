#from django.http import HttpResponse, HttpRequest
from cloudant.client import Cloudant
from datetime import datetime
import datetime as dt
from cloudant.query import Query
from cloudant.result import QueryResult



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
query = Query(my_database,selector= {'_id': {'$gt': 0}, 'd':dt.datetime.now().strftime("%m-%d-%Y")}, fields=['t','temp','d','l'],sort=[{'t': 'desc'}])
temp_dict={}
ALL_temps_dict={}

temp_dict=query(limit=100, skip=0)['docs']
cur_date=dt.datetime.now().strftime("%m-%d-%Y")

if len(temp_dict)>0:

	for row in temp_dict:
		if row['l']=='Familyroom':
			ALL_temps_dict['Familyroom_temp']=row['temp']
			ALL_temps_dict['Familyroom_date']=row['d']
			datetime_object = datetime.strptime(str(row['t']), "%H:%M:%S")
			ALL_temps_dict['Familyroom_time']=datetime_object.strftime("%I:%M %p")
			# print ('found family room record, exiting')
			# print('Familyroom temp is', ALL_temps_dict['Familyroom_temp'], 'read at', ALL_temps_dict['Familyroom_time'], 'on', ALL_temps_dict['Familyroom_date'],'\n')
			familroom_msg='Familyroom temperature is '+str(ALL_temps_dict['Familyroom_temp'])+ u'\N{DEGREE SIGN} read at ' + str(ALL_temps_dict['Familyroom_time']) + ' on ' + str(ALL_temps_dict['Familyroom_date'])
			print (familroom_msg +'\n')
			break

	for row in temp_dict:
		if row['l']=='Garage':
			ALL_temps_dict['Garage_temp']=row['temp']
			ALL_temps_dict['Garage_date']=row['d']
			datetime_object = datetime.strptime(str(row['t']), "%H:%M:%S")
			ALL_temps_dict['Garage_time']=datetime_object.strftime("%I:%M %p")
			# print ('found Garage record, exiting')
			# print('Garage temp is', ALL_temps_dict['Garage_temp'], 'read at', ALL_temps_dict['Garage_time'], 'on', ALL_temps_dict['Garage_date'],'\n')
			garage_msg='Garage temperature is ' + str(ALL_temps_dict['Garage_temp']) + u'\N{DEGREE SIGN} read at ' + str(ALL_temps_dict['Garage_time']) + ' on ' + str(ALL_temps_dict['Garage_date'])
			print(garage_msg +'\n')
			break


	for row in temp_dict:
		if row['l']=='Driveway':
			ALL_temps_dict['Driveway_temp']=row['temp']
			ALL_temps_dict['Driveway_date']=row['d']
			datetime_object = datetime.strptime(str(row['t']), "%H:%M:%S")
			ALL_temps_dict['Driveway_time']=datetime_object.strftime("%I:%M %p")
			# print ('found Driveway record, exiting')
			driveway_msg='Driveway temperature is ' + str(ALL_temps_dict['Driveway_temp']) + u'\N{DEGREE SIGN} read at ' + str(ALL_temps_dict['Driveway_time']) + ' on ' + str(ALL_temps_dict['Driveway_date'])
			print(driveway_msg + '\n') 
			break


	for row in temp_dict:
		if row['l']=='Kitchen':
			ALL_temps_dict['Kitchen_temp']=row['temp']
			ALL_temps_dict['Kitchen_date']=row['d']
			datetime_object = datetime.strptime(str(row['t']), "%H:%M:%S")
			ALL_temps_dict['Kitchen_time']=datetime_object.strftime("%I:%M %p")
			# print ('found Kitchen record, exiting')
			# print('Kitchen temperature is', ALL_temps_dict['Kitchen_temp'], 'read at', ALL_temps_dict['Kitchen_time'], 'on', ALL_temps_dict['Kitchen_date'],'\n')
			kitchen_msg='Kitchen temperature is ' + str(ALL_temps_dict['Kitchen_temp']) + u'\N{DEGREE SIGN} read at ' + str(ALL_temps_dict['Kitchen_time']) +  ' on ' + str(ALL_temps_dict['Kitchen_date'])
			print(kitchen_msg+'\n')
			break

	for row in temp_dict:
		if row['l']=='Basement RPi cabinet':
			ALL_temps_dict['Basement RPi cabinet_temp']=row['temp']
			ALL_temps_dict['Basement RPi cabinet_date']=row['d']
			datetime_object = datetime.strptime(str(row['t']), "%H:%M:%S")
			ALL_temps_dict['Basement RPi cabinet_time']=datetime_object.strftime("%I:%M %p")
			# print ('found Basement RPi cabinet record, exiting')
			basement_rpi_msg='Basement RPi cabinet temperature is ' + str(ALL_temps_dict['Basement RPi cabinet_temp']) + u'\N{DEGREE SIGN} read at ' + str(ALL_temps_dict['Basement RPi cabinet_time']) + ' on ' + str(ALL_temps_dict['Basement RPi cabinet_date'])
			print (basement_rpi_msg+'\n')
			break

	for row in temp_dict:
		if row['l']=='Water Heater':
			ALL_temps_dict['Water Heater_temp']=row['temp']
			ALL_temps_dict['Water Heater_date']=row['d']
			datetime_object = datetime.strptime(str(row['t']), "%H:%M:%S")
			ALL_temps_dict['Water Heater_time']=datetime_object.strftime("%I:%M %p")
			# print ('found Water Heater record, exiting')
			water_heater_msg='Water Heater temperature is '+ str(ALL_temps_dict['Water Heater_temp']) + u'\N{DEGREE SIGN} read at ' + str(ALL_temps_dict['Water Heater_time']) + ' on ' + str(ALL_temps_dict['Water Heater_date'])
			print (water_heater_msg+'\n')
			break

	for row in temp_dict:
		if row['l']=='Backyard':
			ALL_temps_dict['Backyard_temp']=row['temp']
			ALL_temps_dict['Backyard_date']=row['d']
			datetime_object = datetime.strptime(str(row['t']), "%H:%M:%S")
			ALL_temps_dict['Backyard_time']=datetime_object.strftime("%I:%M %p")
			# print ('found Backyard record, exiting')
			backyard_msg='Backyard temperature is ' + str(ALL_temps_dict['Backyard_temp']) + u'\N{DEGREE SIGN} read at ' + str(ALL_temps_dict['Backyard_time']) + ' on ' + str(ALL_temps_dict['Backyard_date'])
			print (backyard_msg,'\n')
			break			




	  # message='NOTE, this ' + str(row['l']) +' temperature was recorded on ' + str(row['d']) +' at ' + str(newdate)  + ' the temperature was: ' + str(row['temp'])
	  # temp1= str(row['temp']) + u"\N{DEGREE SIGN}"
	  # location1=str(row['l'])

	  # print (message)
	  # print (temp1)
	  # print (location1)


# b = {'names': 'TIMOTHY', 'CUR_DATE': str(cur_date),'STATUS1':STATUS1, 'MESSAGE':str(message),'TEMP1':temp1,'LOCATION1':location1}

# for x,y in b.items():
#     html_doc = html_doc.replace(x, y)

# else:
# html_doc = """
# <!DCOTYPE html>
# <html>
# <head>
# <title>Your Better Django Droplet</title>
# <style>
# body {
#     width: 1100px;
#     margin: 0 auto;
#     font-family: Tahoma, Verdana, Arial, sans-serif;
#     background: #AAAAAA;
# }
# div {
#   padding: 30px;
#   background: #FFFFFF;
#   margin: 30px;
#   border-radius: 5px;
#   border: 1px solid #888888;
# }
# pre {
#   padding: 15px;
# }
# code, pre {
#   font-size: 16px;
#   background: #DDDDDD
# }
# </style>
# <body>
# <div>
# <h1>query length is zero</h1>
# <p> debug info:</p>
# <p> the true length is LEN1</p>
# <p> the connection status is: STATUS1</p>




# </div>
# </body>

# """
# b = {'LEN1': str(len(TEMP_DICT)),'STATUS1':STATUS1}

# for x,y in b.items():
# #
# html_doc = html_doc.replace(x, y)

# return HttpResponse(html_doc)
