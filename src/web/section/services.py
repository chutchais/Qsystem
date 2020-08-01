from .models import Section
from job.models import Job

def create_next_queue(section_pk):
	section = Section.objects.get(pk=section_pk)
	# Create Job
	new_job = Job.objects.create(queue_number = section.starting_number + section.current_number,
						section = section)
	print('Create JOB %s ...Done' % new_job)