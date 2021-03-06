from django.db import models
from django.urls import reverse

# Create your models here.

class Counter(models.Model):
	name 			= models.CharField(primary_key=True,max_length=50,null = False)
	counter_number 	= models.IntegerField(default=0)
	current_job 	= models.CharField(max_length=50,blank=True,null = True)
	description 	= models.TextField(null = True,blank = True)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)

	def __str__(self):
		return ('%s' % self.name)

	def get_absolute_url(self):
		return reverse('counter:detail', kwargs={'pk': self.pk})

	def get_working_jobs(self):
		return self.jobs.filter(active=True).select_related('section')

	def get_current_job(self):
		try:
			
			job = self.jobs.filter(active=True,on_process=True).select_related('section')

		except Exception as e:
			job = None
		print(job)
		return job

	class Meta:
		indexes = [
			models.Index(fields=['name'],name='idx_counter_counter_name'),
		]
		ordering = ['counter_number']