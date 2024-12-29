from django.http import HttpResponse, HttpRequest
from cloudant.client import Cloudant
from datetime import datetime
import datetime as dt
from cloudant.query import Query
from cloudant.result import QueryResult

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.dates as mdates



def get_individual_temp(location):
  user_data=get_user_data()
  USERNAME =user_data['cloud_acct_username']
  PASSWORD = user_data['cloud_acct_pword']

  try:
    client = Cloudant(USERNAME,PASSWORD, url = "https://8c1205d4-f169-4cb0-a62e-73d6dba754fb-bluemix:006d4df070101f4d115325956e7f9133a26697c0ab2765c6ed5709f6b26cddbf@8c1205d4-f169-4cb0-a62e-73d6dba754fb-bluemix.cloudantnosqldb.appdomain.cloud" )
    client.connect()
    STATUS1="yes connected!!!!"


  except:
    STATUS1="boo...FAILURE"
    html_doc=html_connection_error()

  TEMP_DICT={}
  my_database = client["temps"]
  query = Query(my_database,selector= {'_id': {'$gt': 0}, 'd':dt.datetime.now().strftime("%m-%d-%Y"), 'l':location}, fields=['t','temp','d','l'],sort=[{'t': 'desc'}])
  TEMP_DICT=query(limit=1, skip=0)['docs']
  cur_date=dt.datetime.now().strftime("%m-%d-%Y")

  if len(TEMP_DICT)>0:
    for row in TEMP_DICT:
       temp= str(row['temp']) + u"\N{DEGREE SIGN}"

  return temp

def get_all_data():

  user_data=get_user_data()
  USERNAME =user_data['cloud_acct_username']
  PASSWORD = user_data['cloud_acct_pword']


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

  html_doc = """
<!DOCTYPE html>
<html>
<title>All Temps</title>
<style>


    body {
        width: 1000px;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
        background: #AAAAAA;
    }
    div {
      padding: 30px;
      background: #FFFFFF;
      margin: 10px;
      border-radius: 5px;
      border: 1px solid #888888;
    }
    pre {
      padding: 15px;
    }
    code, pre {
      font-size: 16px;
      background: #DDDDDD
    }
</style>
</head>
<body>
  <div>
    <h1>These are all the temperature readings</h1>

         <p class=MsoNormal align=left style='text-align:left'><span
style='font-size:12.0pt;font-family:"Arial Rounded MT Bold",sans-serif'> familroom_msg</o:p></span></p>
    <p> garage_msg</p>
    <p> driveway_msg</p>
    <p> kitchen_msg</p>
    <p> basement_rpi_msg</p>
    <p> water_heater_msg</p>
    <p> backyard_msg</p>
    <p></p>
     <p class=MsoNormal align=left style='text-align:left'><span
style='font-size:9.0pt;font-family:"Arial Rounded MT Bold",sans-serif'>this message is coming to you via a simple Django application that's live on my Digital Ocean Droplet! This droplet is all set up with Python, Django, and Postgres. It's also using Gunicorn to run the application on system boot and using nginx to proxy traffic to the application over port 80.<o:p></o:p></span></p>

    
    
  </div>
</body>
</html>
"""

  b = {'familroom_msg': familroom_msg, 'garage_msg': garage_msg,'driveway_msg':driveway_msg, 'kitchen_msg':kitchen_msg,'basement_rpi_msg':basement_rpi_msg,'water_heater_msg':water_heater_msg,'backyard_msg':backyard_msg}
      
  for x,y in b.items():
      html_doc = html_doc.replace(x, y)


  return html_doc









def get_temp_dict(location):

  user_data=get_user_data()
  USERNAME =user_data['cloud_acct_username']
  PASSWORD = user_data['cloud_acct_pword']

  try:
    client = Cloudant(USERNAME,PASSWORD, url = "https://8c1205d4-f169-4cb0-a62e-73d6dba754fb-bluemix:006d4df070101f4d115325956e7f9133a26697c0ab2765c6ed5709f6b26cddbf@8c1205d4-f169-4cb0-a62e-73d6dba754fb-bluemix.cloudantnosqldb.appdomain.cloud" )
    client.connect()
    STATUS1="yes connected!!!!"


  except:
    STATUS1="boo...FAILURE"
    html_doc=html_connection_error()

  TEMP_DICT={}
  my_database = client["temps"]
  query = Query(my_database,selector= {'_id': {'$gt': 0}, 'd':dt.datetime.now().strftime("%m-%d-%Y"), 'l':location}, fields=['t','temp','d','l'],sort=[{'t': 'desc'}])
  TEMP_DICT=query(limit=1000, skip=0)['docs']
  cur_date=dt.datetime.now().strftime("%m-%d-%Y")

  df = pd.DataFrame(temp_dict)
  df.t = pd.to_datetime(df.t)




  if len(TEMP_DICT)>0:
    for row in TEMP_DICT:
      datetime_object = datetime.strptime(str(row['t']), "%H:%M:%S")
      newdate = datetime_object.strftime("%I:%M:%S %p")


      message='NOTE, this ' + str(row['l']) +' temperature WAS recorded on ' + str(row['d']) +' at ' + str(newdate)  + ' the temperature was: ' + str(row['temp'])
      temp1= str(row['temp']) + u"\N{DEGREE SIGN}"
      location1=str(row['l'])

      html_doc=html_status_page()

      b = {'names': 'TIMOTHY', 'CUR_DATE': str(cur_date),'STATUS1':STATUS1, 'MESSAGE':str(message),'TEMP1':temp1,'LOCATION1':location1}
      
      for x,y in b.items():
          html_doc = html_doc.replace(x, y)

      break

  else:
    html_doc=html_zero_len()
    b = {'LEN1': str(len(TEMP_DICT)),'STATUS1':STATUS1, 'SYSTEMDATE1':dt.datetime.now().strftime("%m-%d-%Y")}
    for x,y in b.items():
      html_doc = html_doc.replace(x, y)

  plt.figure(figsize=(15,15))
  g=sns.lineplot(x='t', y='temp', data=df,color="darkblue")

  plt.ylim(df['temp'].min()-1, df['temp'].max()+1)
  plt.xticks(rotation=45)
  # compensate for axis labels getting clipped off
  plt.subplots_adjust(bottom=.5, left=0.15)

  g.xaxis.set_major_formatter(mdates.DateFormatter('%I'))


  #g.xaxis.set_major_locator(mdates.HourLocator(interval = 5))
  g.set(xlabel='Time', ylabel='Temperature')

  #create unique filename based on time
  #filename= "Graph-" +str(dt.datetime.now().hour)+"-"+str(dt.datetime.now().minute)+".png"
  filename="/home/django/django_project/django_project/GRAPH_" + location + ".png"
  plt.savefig(filename)


  return html_doc



def get_user_data():
  user_data = {}
  with open("/home/django/django_project/django_project/django.txt") as f:
    for line in f:
      (field, val) = line.split()
      user_data[field] = val

  return user_data


def gen_html_test_msg():

  test_html = """
<!DOCTYPE html>
<html>
<head>
<title>TITLE: test page</title>
<style>
    body {
        width: 1000px;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
        background: #AAAAAA;
    }
    div {
      padding: 30px;
      background: #FFFFFF;
      margin: 30px;
      border-radius: 5px;
      border: 1px solid #888888;
    }
    pre {
      padding: 15px;
    }
    code, pre {
      font-size: 16px;
      background: #DDDDDD
    }
</style>
</head>
<body>
  <div>
    <h1>BEEEEETTER TEST PAGE</h1>
  </div>
</body>
</html>
"""
  return test_html  

def html_zero_len():

  zero_len_html_doc = """
<!DCOTYPE html>
<html>
<head>
<title>Your Better Django Droplet</title>
<style>
    body {
        width: 1100px;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
        background: #AAAAAA;
    }
    div {
      padding: 30px;
      background: #FFFFFF;
      margin: 30px;
      border-radius: 5px;
      border: 1px solid #888888;
    }
    pre {
      padding: 15px;
    }
    code, pre {
      font-size: 16px;
      background: #DDDDDD
    }
</style>
<body>
  <div>
    <h1>query length is zero</h1>
    <p> debug info:</p>
    <p> the true length is LEN1</p>
    <p> the connection status is: STATUS1</p>
    <p> the system date is: SYSTEMDATE1</p>





  </div>
</body>
"""
  return zero_len_html_doc


def html_connection_error():
  html_doc = """
<!DCOTYPE html>
<html>
<head>
<title>Your Better Django Droplet</title>
<style>
    body {
        width: 1100px;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
        background: #AAAAAA;
    }
    div {
      padding: 30px;
      background: #FFFFFF;
      margin: 30px;
      border-radius: 5px;
      border: 1px solid #888888;
    }
    pre {
      padding: 15px;
    }
    code, pre {
      font-size: 16px;
      background: #DDDDDD
    }
</style>
<body>
  <div>
    <h1>READ FAILURE</h1>



  </div>
</body>

  """
  return html_doc

def html_status_page():

    html_doc = """
<!DCOTYPE html>
<html>
<head>
<title>LOCATION1</title>
<style>
    body {
        width: 1100px;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
        background: #AAAAAA;
    }
    div {
      padding: 30px;
      background: #FFFFFF;
      margin: 30px;
      border-radius: 5px;
      border: 1px solid #888888;
    }
    pre {
      padding: 15px;
    }
    code, pre {
      font-size: 16px;
      background: #DDDDDD
    }
</style>
<body>
  <div>
    <h1>LOCATION1 temperature</h1>


  <p class=MsoNormal align=center style='text-align:center'><span
style='font-size:300.0pt;font-family:"Arial Rounded MT Bold",sans-serif'>TEMP1<o:p></o:p></span></p>

    <p>MESSAGE</p>


    <p> </p>
    <p>
</body>
  """
    return html_doc

# def index_html():






#   return html_doc


#####removed above: <li>SSH into your Droplet. <pre><code>ssh root@{IPADDRESS}</code></pre></li>

####################################
####################################

#def gen_error_html_msg():





# def gen_html_test_msg():

#   test_html = """
# <!DOCTYPE html>
# <html>
# <head>
# <title>TITLE=test page</title>
# <style>
#     body {
#         width: 1000px;
#         margin: 0 auto;
#         font-family: Tahoma, Verdana, Arial, sans-serif;
#         background: #AAAAAA;
#     }
#     div {
#       padding: 30px;
#       background: #FFFFFF;
#       margin: 30px;
#       border-radius: 5px;
#       border: 1px solid #888888;
#     }
#     pre {
#       padding: 15px;
#     }
#     code, pre {
#       font-size: 16px;
#       background: #DDDDDD
#     }
# </style>
# </head>
# <body>
#   <div>
#     <h1>TEST PAGE</h1>
#   </div>
# </body>
# </html>
# """
#   return test_html  


# = 'This is a test string.'






