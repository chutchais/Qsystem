import schedule
import time
from datetime import datetime, timedelta
import redis
import json
# from task import play_call_sound

# db = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
db = redis.StrictRedis('192.168.99.100', 6379, charset="utf-8", decode_responses=True)
# db = redis.StrictRedis('10.24.50.93', 6379, charset="utf-8", decode_responses=True) #Production


def pulling_q():
	# try:
	now = datetime.now() # current date and time
	# start_time 	= get_last_exe_time('B1')
	stop_time 	= now.strftime("%Y-%m-%d %H:%M:%S")
	for q in db.keys('P*'):
		counter = q.split(':')[1]
		payload = json.loads(db.get(q))
		prefix = payload['prefix']
		number = payload['number']
		wait   = payload['wait']
		date   = payload['date']
		number = int(number)
		# print('Print Q :' ,number )
		# print(prefix)
		# delete key
		db.delete(q)
		print('Print Q : %s%03d  -- Date : %s Waiting Q : %s' % (prefix,number,date,wait))

		make_print_file('%s%03d' % (prefix,number))
		import os
		myCmd = 'senddat.exe -t q.txt USBPRN0' 
		print(myCmd)
		import subprocess
		subprocess.call(myCmd)
	# except Exception as e:
	# 	pass
	


def make_print_file(q_number):
	try:
		f = open("q.txt","w+")
		# f.write("This is line %s\r\n" % q_number)
		f.write("ESC a 1\r\n")
		f.write("GS ! 0\r\n")
		f.write('\r\n')
		f.write('"LCB1&LCMT Q-System" CR LF\r\n')
		f.write('GS ! 119\r\n')
		f.write('"%s" CR LF\r\n' % q_number)
		f.write('GS ! 0\r\n')
		f.write('CR LF\r\n')
		f.write('CR LF\r\n')
		f.write('CR LF\r\n')
		f.write('CR LF\r\n')
		f.write('GS V 0\r\n')
		f.write('*1000\r\n')
	except Exception as e:
		pass
	


	f.close() 
		# play_call_sound(number,counter,prefix)
		# print (counter,prefix,number)
	# print(db.keys('Q*'))
	# print(f"Pulling data of B1. from {get_last_exe_time('B1')} to {datetime.now()}")
	# print(f"New TruckQ : {pulling_PAT(b1_json)} records")


schedule.every(1).seconds.do(pulling_q)
# schedule.every(5).minutes.do(pulling_a0)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

# Initial run
pulling_q()

#------------
while True:
	try:
		schedule.run_pending()
		time.sleep(1)
	except Exception as e:
		pass
	
