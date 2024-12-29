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
query = Query(my_database,selector= {'_id': {'$gt': 0}, 'd':dt.datetime.now().strftime("%m-%d-%Y"), 'l':'Backyard'}, fields=['t','temp','d','l'],sort=[{'t': 'desc'}])
temp_dict={}

temp_dict=query(limit=1, skip=0)['docs']
cur_date=dt.datetime.now().strftime("%m-%d-%Y")
TEMP_DICT=temp_dict

if len(TEMP_DICT)>0:

	for row in TEMP_DICT:
	  datetime_object = datetime.strptime(str(row['t']), "%H:%M:%S")
	  #newdate = datetime.strptime(str(datetime_object), "%I:%M:%S %p")
	  newdate = datetime_object.strftime("%I:%M:%S %p")


	  message='NOTE, this ' + str(row['l']) +' temperature was recorded on ' + str(row['d']) +' at ' + str(newdate)  + ' the temperature was: ' + str(row['temp'])
	  temp1= str(row['temp']) + u"\N{DEGREE SIGN}"
	  location1=str(row['l'])

	  print (message)
	  print (temp1)
	  print (location1)


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
