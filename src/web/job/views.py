from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy

from .models import Job
from counter.models import Counter
from django.utils import timezone
from django.conf import settings

# from .tasks import play_call_sound

# Redis

import time
import json
import redis
db = redis.StrictRedis('redis', 6379, charset="utf-8", decode_responses=True)

from django_q.tasks import async_task

class JobListView(LoginRequiredMixin,ListView):
	model = Job

class JobDetailView(LoginRequiredMixin,DetailView):
	model = Job

class JobDeleteView(LoginRequiredMixin,DeleteView):
	model = Job
	success_url = reverse_lazy('counter:list')





def call_job(self,job_pk):
	job = Job.objects.get(pk=job_pk)
	counter = job.counter

	add_q(counter.counter_number,job.section.prefix,job.queue_number)

	return HttpResponseRedirect('%s?section=%s' % (reverse('counter:detail',kwargs={'pk': counter.pk}),job.section)) 


def assign_counter(self,job_pk,counter_pk):
	job = Job.objects.get(pk=job_pk)
	# counter = Counter.objects.get(pk=counter_pk)
	# # Assign counter to Job
	# job.counter =  counter
	# job.started_date = timezone.now()
	# job.on_process=True
	# job.save()

	# counter.current_job = job.get_full_name()
	# counter.save()

	counter = Counter.objects.get(pk=counter_pk)
	# enqueue the task
	jobWithCounterPk = '%s||%s' % (job_pk,counter_pk)
	async_task("job.services.assign_counter", jobWithCounterPk)
	#
	
	# Save to Database(Redis)
	add_q(counter.counter_number,job.section.prefix,job.queue_number)
	# ---------
	return HttpResponseRedirect('%s?section=%s' % (reverse('counter:detail',kwargs={'pk': counter.pk}),job.section)) 

def cancel_job(self,job_pk):
	job = Job.objects.get(pk=job_pk)
	counter = job.counter
	# counter.current_job = None
	# counter.save()

	# job.counter =  None
	# job.started_date = None
	# job.on_process=False
	# job.save()
	# enqueue the task
	async_task("job.services.cancel_job", job)
	#

	
	url = '%s?section=%s' % (reverse('counter:detail',kwargs={'pk': counter.pk}),job.section)
	return HttpResponseRedirect(url) 

def complete_job(request,job_pk):
	print(request.user)
	job = Job.objects.get(pk=job_pk)
	counter = job.counter
	url = '%s?section=%s' % (reverse('counter:detail',kwargs={'pk': counter.pk}),job.section)


	# counter.current_job = None
	# counter.save()
	# job.active = False
	# job.on_process=False
	# job.finished_date = timezone.now()
	# job.save()
	# enqueue the task
	async_task("job.services.complete_job", job_pk,request.user)
	#
	return HttpResponseRedirect(url) 


def add_q(counter,q_prefix,q_number):
	# Save to Database
	ttl = 60*60 #1 minutes
	key = f"Q:{counter}"
	payload ={
		"prefix":q_prefix,
		"number":q_number,
	}
	# Revove for import speed
	# if db.exists(key):
	# 	db.delete(key)
	
	db.set(key,json.dumps(payload)) #store dict in a hashjson.dumps(json_data)
	db.expire(key, ttl) #expire it after a year
