from time import sleep

import json
from django.utils import timezone
# import redis
# db = redis.StrictRedis('192.168.99.100', 6379, charset="utf-8", decode_responses=True)

def sleep_and_print(secs):
	sleep(secs)
	print("Task ran!")

# Job Action
from .models import Job,Job_Archive
from counter.models import Counter

def cancel_job(job):
	# job = Job.objects.get(pk=job_pk)
	counter = job.counter
	counter.current_job = None
	counter.save()

	job.counter =  None
	job.started_date = None
	job.on_process=False
	job.user=None
	job.save()
	print('Cancel JOB %s ...Done' % job)

def assign_counter(jobWithCounterPk):
	job_pk		= jobWithCounterPk.split('||')[0]
	counter_pk  = jobWithCounterPk.split('||')[1]
	job = Job.objects.get(pk=job_pk)
	counter = Counter.objects.get(pk=counter_pk)
	# Assign counter to Job
	job.counter =  counter
	job.started_date = timezone.now()
	job.on_process=True
	job.save()

	counter.current_job = job.get_full_name()
	counter.save()
	print('Assign JOB %s ...Done' % job)

def complete_job(job_pk,user_obj):
	job = Job.objects.get(pk=job_pk)
	counter = job.counter
	counter.current_job = None
	counter.save()

	job.active = False
	job.on_process=False
	job.finished_date = timezone.now()
	job.user = user_obj
	job.save()

	import math
	# Added on Jan 21,2021 -- TO copy job to Job Archive
	import datetime, pytz
	from django.utils.timezone import localtime
	tz = pytz.timezone('Asia/Bangkok')
	create_dt = localtime(job.created_date) #.replace(tzinfo=tz)
	local_dt = datetime.datetime.now(tz=tz)
	waiting_time= math.ceil((job.started_date - job.created_date).total_seconds() / 60.0)
	process_time= math.ceil((job.finished_date - job.started_date).total_seconds() / 60.0)
	total_time = waiting_time+process_time
	job_archive = Job_Archive(queue_number=job.queue_number,section=job.section,counter=job.counter,
					on_process=job.on_process,note=job.note,created_date=job.created_date,
					modified_date=job.modified_date,started_date=job.started_date,finished_date=job.finished_date,
					active=job.active,user=job.user,
					year_arch=create_dt.year,month_arch=create_dt.month,
					day_created=create_dt.day,hour_created=create_dt.hour,
					day_completed=local_dt.day,hour_completed=local_dt.hour,
					waiting_time	= waiting_time,
					process_time	= process_time,
					total_time 		= total_time
					)
	job_archive.save()

	# Added on Jan 21,2021 -- To delete job 
	job.delete()

	print('Complete JOB %s ...Done' % job_archive)
# def add_q(playloadWithKey):

# 	ttl = 60*60 #1 minutes
# 	key 	= 	playloadWithKey.split('||')[0]
# 	payload =	playloadWithKey.split('||')[1]
# 	if db.exists(key):
# 		db.delete(key)
# 	db.set(key,json.dumps(payload)) #store dict in a hashjson.dumps(json_data)
# 	db.expire(key, ttl) #expire it after a year
# 	print(redis)
# 	print('Add Q JOB %s - %s ...Done' % (key,payload))