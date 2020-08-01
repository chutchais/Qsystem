from time import sleep

import json
from django.utils import timezone
# import redis
# db = redis.StrictRedis('192.168.99.100', 6379, charset="utf-8", decode_responses=True)

def sleep_and_print(secs):
    sleep(secs)
    print("Task ran!")

# Job Action
from .models import Job
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
	print('Complete JOB %s ...Done' % job)
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