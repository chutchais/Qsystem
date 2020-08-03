from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Counter
from job.models import Job
from section.models import Section

class CounterListView(LoginRequiredMixin,ListView):
	model = Counter

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pending_job_list'] = Job.objects.filter(
			active=True,on_process=False).select_related('section')[:30]
		# context['current_job'] ='My job'
		return context

class CounterDetailView(LoginRequiredMixin,DetailView):
	model = Counter

	def get_context_data(self, **kwargs):
		query = self.request.GET.get('section')
		context = super().get_context_data(**kwargs)
		counter = super().get_object()
		
		context['working_job_list'] = Job.objects.filter(
			counter=counter, active=True,on_process=True).select_related('section')[:5]
		# context['working_job_list'] = Job.objects.filter(active=True,
		# 				on_process=True,counter=counter).select_related('section').values_list(
		# 				'id','queue_number','section__color','section__prefix','created_date')

		# print(query)
		# Job.objects.filter(
		#active=True,on_process=False,section__name='section1',counter=None)
		#.select_related('section').values_list('id','queue_number','section__color','section__prefix','created_date')
		if query :
			context['pending_job_list'] = Job.objects.filter(
				active=True,on_process=False,section__name=query,counter=None).select_related('section')[:20]
		else :
			context['pending_job_list'] = Job.objects.filter(
				active=True,on_process=False,counter=None).select_related('section')[:50]
		
		context['section_list'] = Section.objects.all()
		return context