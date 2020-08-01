from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
import datetime
from django.conf import settings

# @login_required
# def index(request):
#     fname = "product/index.html"
#     product_list = Product.objects.filter(
#     					active = True,modified_date__gt= datetime.datetime.today()-datetime.timedelta(days=30)
#     					).order_by('group','name')
#     return render(
# 			request,
# 			fname,
# 			{
# 				'object_list' : product_list
# 			}
# 		)

# from .models import Product,ProductGroup

# class ProductListView(LoginRequiredMixin,ListView):
# 	model = Product
# 	paginate_by = 100

# 	def get_queryset(self):
# 		query = self.request.GET.get('q')
# 		if query :
# 			return Product.objects.filter(Q(name__icontains=query) |
# 									Q(fg_name__icontains=query) |
# 									Q(description__icontains=query) |
# 									Q(customer__name__icontains=query)|
# 									Q(parent__name__icontains=query) |
# 									Q(group__name__icontains=query) ).order_by('-created_date')
# 		return Product.objects.all()
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Section
from job.models import Job

import json
import redis
db = redis.StrictRedis('redis', 6379, charset="utf-8", decode_responses=True)

from django_q.tasks import async_task

class SectionListView(LoginRequiredMixin,ListView):
	model = Section

class SectionDetailView(LoginRequiredMixin,DetailView):
	model = Section

def create_next_queue(self,pk):
	# enqueue the task
	section = Section.objects.get(pk=pk)
	section.create_queue()
	async_task("section.services.create_next_queue", pk)
	#

	# section = Section.objects.get(pk=pk)
	# section.create_queue()
	# new_job = Job.objects.create(queue_number = section.starting_number + section.current_number,
	# 					section = section)
	# print Queue paper
	# Send Q number to print.
	qnumber = '%s%s' % (section.starting_number ,section.current_number)
	print(qnumber)
	add_print(section.prefix,qnumber)
	# ----------

	return HttpResponseRedirect(reverse('section:list'))

def add_print(q_prefix,q_number):
	# Save to Database
	ttl = 60*60 #1 minutes
	key = f"P:{q_number}"
	payload ={
		"prefix":q_prefix,
		"number":q_number,
	}
	if db.exists(key):
		db.delete(key)
	db.set(key,json.dumps(payload)) #store dict in a hashjson.dumps(json_data)
	db.expire(key, ttl) #expire it after a year

def make_print_file(q_number):
	pth = settings.STATIC_ROOT
	f = open("%sq1.txt" % pth,"w+")
	# f.write("This is line %s\r\n" % q_number)
	f.write("ESC a 1\r\n")
	f.write("GS ! 0\r\n")
	f.write('\r\n')
	f.write('"LCB1&LCMT Q-System" CR LF\r\n')
	f.write('GS ! 119\r\n')
	f.write('"%s" CR LF\r\n' % q_number)
	f.write('GS ! 0\r\n')
	f.write('CR LF\r\n')
	f.write('CR LF\r\n')
	f.write('CR LF\r\n')
	f.write('CR LF\r\n')
	f.write('GS V 0\r\n')
	f.write('*1000\r\n')


	f.close() 


# class ProductGroupListView(LoginRequiredMixin,ListView):
# 	model = ProductGroup

# class ProductGroupDetailView(LoginRequiredMixin,DetailView):
# 	model = ProductGroup