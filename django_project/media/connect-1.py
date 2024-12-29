import pymysql
import logging
import sshtunnel
from sshtunnel import SSHTunnelForwarder
import paramiko

ssh_host = '206.81.2.218'
ssh_username = 'root'
ssh_password = '27Kovelov'
database_username = 'hms'
database_password = '27Kovelov!'
database_name = 'temps'
localhost = '127.0.0.1'

# conn = pymysql.connect(
#     host='206.81.2.218',
#     user='hms', 
#     password = "27Kovelov!",
#     db='temps',
#     )
  
# cur = conn.cursor()
# cur.execute("select @@version")
# output = cur.fetchall()
# print(output)
  
# # To close the connection
# conn.close()

print ('stuff loaded')

global tunnel
tunnel = SSHTunnelForwarder(
    (ssh_host, 22),
    ssh_pkey=paramiko.agent.Agent().get_keys(),
    ssh_username = ssh_username,
    ssh_password = ssh_password,
    remote_bind_address = ('127.0.0.1', 3306),

)

print ('connection made')

tunnel.start()



global connection

connection = pymysql.connect(
    host='127.0.0.1',
    user=database_username,
    passwd=database_password,
    db=database_name,
    port=tunnel.local_bind_port
)



print ('connection made to mysql')










