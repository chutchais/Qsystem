from .models import Section
from job.models import Job
from counter.models import Counter

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
	print('Reset Section current Queue...')
