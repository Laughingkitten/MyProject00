from kafka import KafkaConsumer, KafkaProducer
import MySQLdb

conn = MySQLdb.connect(
	user='USERNAME',
	passwd='PASSWORD',
	host='HOSTNAME',
	db='DBNAME'
)
c = conn.cursor()


def insert_sql(idm,Name,RaspiID,timestamp):
	sql = 'insert into demo values(%s,%s,%s,%s)'
	c.execute(sql,(idm,Name,RaspiID,timestamp))
	cnn.commit()



def get_name(idm):
	sql = 'select name from demouser where idm=%s'
	c.execute(sql,[idm])
	result = c.fetchall()
	result = str(result[0])
	result = result.split(",")
	result = result[0]
	result = result.replace("(","")
	return result
	#c.commit()

def get_num(idm):
	sql = 'select uid from ldap_idm where edyid=%s'
	c.execute(sql,[idm])
	result = c.fetchall()
	result = str(result[0])
	result = result.split(",")
	result = result[0]
	result = result.replace("(","")
	return result
	#c.commit()





def main():
	consumer = KafkaConsumer(bootstrap_servers='IPADDR:9092',auto_offset_reset='earliest')
	consumer.subscribe(['TOPICNAME'])

	for message in consumer:
		message = str(message)
		message = message.split(",")
		print message
		idm = message[6].split("=")
		idm = idm[1].split("'")
		idm = idm[1]
		print('idm:',idm)

		#Name = message[7].split("u")
		#Name = Name[1].replace("'","")
		#print('Name:',Name)

		name = get_name(idm)
		print("NAME: ",name)

		#uid = get_num(idm)
		uid = 'testnum'

		room = message[7]
		print('ROOM:',room)

		roomkey = message[8].split(")")
		roomkey = roomkey[0].replace(" u","").replace("'","")
		print('ROOMKEY:',roomkey)

		timestamp = message[9].replace("\"","")
		timestamp = timestamp.replace("\'","")
		print('TIMESTAMP:',timestamp)
		
		sql = 'insert testhead01(idm,name,uid,room,roomkey,ts) values(%s,%s,%s,%s,%s,%s)'
		c.execute(sql,(idm,name,uid,room,roomkey,timestamp))
		conn.commit()

	

		#return idm,Name,timestamp,RaspiID


if __name__ == "__main__":
    main()
    #idm = '3001011501160155'
    #name=get_name(idm)
    #print(name)
    #print(get_num(idm))
    
