import mysql.connector

db_user = "rt"
db_password = "RT@pipe18@"
db_host = "127.0.0.1"
db_port = "63306"
db_name = "rt_alert_db"


connector = mysql.connector.connect(user=db_user, password=db_password,host=db_host, port=db_port, database=db_name)
cursor = connector.cursor()


query = "SELECT ins.name AS instrument_name, max(n.seqnum),n.noticetime, n.receivedsciencealertid, rsa.triggerid,rsa.ste,rsa.time as `trigger_time` from notice n join correlations c on (n.receivedsciencealertid = c.rsaId2) join receivedsciencealert rsa on ( rsa.receivedsciencealertid = n.receivedsciencealertid) join instrument ins on (ins.instrumentid = rsa.instrumentid) where c.rsaId1 = 10280  group by n.receivedsciencealertid" 
cursor.execute(query)
results_row = cursor.fetchall()

print(type(results_row))
print(results_row)

