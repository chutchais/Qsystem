from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
from section.models import Section
from counter.models import Counter

class Job(models.Model):
	queue_number	= models.IntegerField(default=0)
	section			= models.ForeignKey(Section,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'jobs')
	counter			= models.ForeignKey(Counter,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'jobs')
	on_process		= models.BooleanField(default=False)
	note 			= models.TextField(null = True,blank = True)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	started_date	= models.DateTimeField(blank=True, null=True)
	finished_date	= models.DateTimeField(blank=True, null=True)
	active			= models.BooleanField(default=True)
	user 			= models.ForeignKey(
							settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,
							blank=True, null=True,
							related_name = 'jobs'
						)

	def __str__(self):
		return ('Oueue : %s of %s' % (self.queue_number,self.section))

	def get_full_name(self):
		return '%s%03d' % (self.section.prefix, self.queue_number)

	def get_absolute_url(self):
		return reverse('job:detail', kwargs={'pk': self.pk})

	class Meta:
		indexes = [
			models.Index(fields=['counter'],name='idx_job_job_counter'),
			models.Index(fields=['section'],name='idx_job_job_section'),
			models.Index(fields=['active'],name='idx_job_job_active'),
		]
		ordering = ['created_date']



# Added on Jan 21,2021 -- To archive Job
class Job_Archive(models.Model):
	queue_number	= models.IntegerField(default=0)
	section			= models.ForeignKey(Section,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'jobs_archive')
	counter			= models.ForeignKey(Counter,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'jobs_archive')
	on_process		= models.BooleanField(default=False)
	note 			= models.TextField(null = True,blank = True)
	created_date	= models.DateTimeField(blank=True, null=True)#Remove auto_now_add on Feb 9,2021
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	started_date	= models.DateTimeField(blank=True, null=True)
	finished_date	= models.DateTimeField(blank=True, null=True)
	active			= models.BooleanField(default=True)
	user 			= models.ForeignKey(
							settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,
							blank=True, null=True,
							related_name = 'jobs_archive'
						)
	year_arch 			= models.IntegerField(default=0)
	month_arch			= models.IntegerField(default=0)
	day_created			= models.IntegerField(default=0)
	hour_created		= models.IntegerField(default=0)
	day_completed		= models.IntegerField(default=0)
	hour_completed		= models.IntegerField(default=0)
	waiting_time		= models.IntegerField(default=0)
	process_time		= models.IntegerField(default=0)
	total_time			= models.IntegerField(default=0)

	def __str__(self):
		return ('Oueue : %s of %s' % (self.queue_number,self.section))

	def get_full_name(self):
		return '%s%03d' % (self.section.prefix, self.queue_number)

	def get_absolute_url(self):
		return reverse('job:archive', kwargs={'pk': self.pk})

	class Meta:
		indexes = [
			models.Index(fields=['counter'],name='idx_job_archive_job_counter'),
			models.Index(fields=['section'],name='idx_job_archive_job_section'),
			models.Index(fields=['active'],name='idx_job_archive_job_active'),
		]
		ordering = ['-created_date']
