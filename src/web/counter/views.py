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
		context['job_list'] = Job.objects.filter(active=True , counter=None)
		return context

class CounterDetailView(LoginRequiredMixin,DetailView):
	model = Counter

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['job_list'] = Job.objects.filter(active=True)
		return context