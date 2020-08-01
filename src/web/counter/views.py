from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Counter
from job.models import Job

class CounterListView(LoginRequiredMixin,ListView):
	model = Counter

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pending_job_list'] = Job.objects.filter(
			active=True,on_process=False).select_related('section','counter')[:30]
		# context['current_job'] ='My job'
		return context

class CounterDetailView(LoginRequiredMixin,DetailView):
	model = Counter

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		counter = super().get_object()
		context['working_job_list'] = Job.objects.filter(
			counter=counter, active=True,on_process=True).select_related('section','counter')[:5]
		context['pending_job_list'] = Job.objects.filter(
			active=True,on_process=False).select_related('section','counter')[:30]
		# context['job_list'] = Job.objects.filter(active=True,counter=counter).select_related('section','counter')
		return context