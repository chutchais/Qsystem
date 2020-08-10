from django.db import models
from django.urls import reverse


# Create your models here.
class Section(models.Model):
	name 			= models.CharField(primary_key=True,max_length=50,null = False)
	description 	= models.TextField(null = True,blank = True)
	prefix 			= models.CharField(max_length=1,null = False,blank = True)
	starting_number = models.IntegerField(default=0)
	maximum_number	= models.IntegerField(default=200)
	current_number	= models.IntegerField(default=0)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)
	color			= models.CharField(max_length=20,null = False,blank = True)
	seq 			= models.IntegerField(default=10)

	def __str__(self):
		return ('%s' % self.name)

	def get_absolute_url(self):
		return reverse('section:detail', kwargs={'pk': self.pk})

	def get_actual_number(self):
		return self.starting_number + self.current_number

	
	def create_queue(self):
		if self.current_number + 1 > self.maximum_number:
			self.current_number = 1
		else :
			self.current_number = self.current_number + 1
		self.save()

	class Meta:
		indexes = [
			models.Index(fields=['name'],name='idx_section_section_name'),
		]
		ordering = ['seq']
