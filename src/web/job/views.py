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
import json
import redis
db = redis.StrictRedis('redis', 6379, charset="utf-8", decode_responses=True)

class JobListView(LoginRequiredMixin,ListView):
	model = Job

class JobDetailView(LoginRequiredMixin,DetailView):
	model = Job

class JobDeleteView(LoginRequiredMixin,DeleteView):
	model = Job
	success_url = reverse_lazy('counter:list')


import threading
import time

class myThread (threading.Thread):
   def __init__(self, job_number, counter_number, job_prefix):
      threading.Thread.__init__(self)
      self.job_number = job_number
      self.counter_number = counter_number
      self.job_prefix = job_prefix
   def run(self):
      print ("Starting :" + str(self.job_number))
      # Get lock to synchronize threads
      # threadLock.acquire()
      play_call_sound(self.job_number, self.counter_number,self.job_prefix)
      # Free lock to release next thread
      # threadLock.release()

def call_job(self,job_pk):
	job = Job.objects.get(pk=job_pk)
	counter = job.counter
	# counter = Counter.objects.get(pk=counter_pk)
	# thread1 = myThread(job.queue_number,counter.counter_number,job.section.prefix)
	# thread1.start()
	add_q(counter.counter_number,job.section.prefix,job.queue_number)
	# play_call_sound(job,counter,job.section.prefix)
	# ---------
	# print (counter.id)
	return HttpResponseRedirect(reverse('counter:detail',kwargs={'pk': counter.pk})) 


def assign_counter(self,job_pk,counter_pk):
	job = Job.objects.get(pk=job_pk)
	counter = Counter.objects.get(pk=counter_pk)
	# Assign counter to Job
	job.counter =  counter
	job.started_date = timezone.now()
	job.save()
	# ----------
	# Should be another thread
	# thread1 = myThread(job.queue_number,counter.counter_number,job.section.prefix)
	# thread1.start()
	# Save to Database(Redis)
	add_q(counter.counter_number,job.section.prefix,job.queue_number)
	# play_call_sound(job.queue_number,counter.counter_number,job.section.prefix)
	# ---------
	return HttpResponseRedirect(reverse('counter:detail',kwargs={'pk': counter.pk})) 

def cancel_job(self,job_pk):
	job = Job.objects.get(pk=job_pk)
	counter = job.counter
	url = reverse('counter:detail',kwargs={'pk': counter.pk})
	job.counter =  None
	job.started_date = None
	job.save()
	return HttpResponseRedirect(url) 

def complete_job(self,job_pk):
	job = Job.objects.get(pk=job_pk)
	counter = job.counter
	url = reverse('counter:detail',kwargs={'pk': counter.pk})
	job.active = False
	job.finished_date = timezone.now()
	job.save()
	return HttpResponseRedirect(url) 


def add_q(counter,q_prefix,q_number):
	# Save to Database
	ttl = 60*60 #1 minutes
	key = f"Q:{counter}"
	payload ={
		"prefix":q_prefix,
		"number":q_number,
	}
	if db.exists(key):
		db.delete(key)
	db.set(key,json.dumps(payload)) #store dict in a hashjson.dumps(json_data)
	db.expire(key, ttl) #expire it after a year
