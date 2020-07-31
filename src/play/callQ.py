import schedule
import time
from datetime import datetime, timedelta
import redis
import json
from task import play_call_sound

# db = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)

db = redis.StrictRedis('192.168.99.100', 6379, charset="utf-8", decode_responses=True) # Dockere
# db = redis.StrictRedis('10.24.50.94', 6379, charset="utf-8", decode_responses=True) #Production

def pulling_q():
	now = datetime.now() # current date and time
	# start_time 	= get_last_exe_time('B1')
	stop_time 	= now.strftime("%Y-%m-%d %H:%M:%S")
	for q in db.keys('Q*'):
		counter = q.split(':')[1]
		payload = json.loads(db.get(q))
		prefix = payload['prefix']
		number = payload['number']
		# delete key
		db.delete(q)
		
		play_call_sound(number,counter,prefix)
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
	schedule.run_pending()
	time.sleep(1)
