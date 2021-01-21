from .models import Section
from job.models import Job
from counter.models import Counter

import time
import json
import redis
db = redis.StrictRedis('redis', 6379, charset="utf-8", decode_responses=True)

def create_next_queue(section_pk):
	section = Section.objects.get(pk=section_pk)
	# Create Job
	new_job = Job.objects.create(queue_number = section.starting_number + section.current_number,
						section = section)
	print('Create JOB %s ...Done' % new_job)


# Daily Schedule Task to reset count
def reset_queue():
	Section.objects.update(current_number=0)
	Counter.objects.update(current_job='')
	# Added on Aug 19,2020 -- To delete all Job. (found speed problem)
	Job.objects.all().delete()
	# current_job

	# Added on Nov 26,2020 -- To initial data to Redis (current_number , prefix,color)
	sync_section_to_redis()

	print('Reset Section current Queue...')


# Added on Nov 26,2020 -- To sync Db with Redis
# Hookable from section update.
def sync_section_to_redis():
	# key = f'section:{section}:current'
	# key = f'section:{section}:prefix'
	# key = f'section:{section}:color'
	sections =  Section.objects.all()
	for section in sections :
		key = f'section:{section}:current'
		db.set(key,section.current_number)
		key = f'section:{section}:prefix'
		db.set(key,section.prefix)
		key = f'section:{section}:color'
		db.set(key,section.color)
	print('Sync Section data success')


