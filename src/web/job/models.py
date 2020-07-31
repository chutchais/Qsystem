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
	note 			= models.TextField(null = True,blank = True)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	started_date	= models.DateTimeField(blank=True, null=True)
	finished_date	= models.DateTimeField(blank=True, null=True)
	active			= models.BooleanField(default=True)
	user 			= models.ForeignKey(
							settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,
							blank=True, null=True
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
		]
		ordering = ['created_date']

