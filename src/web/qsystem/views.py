from django.shortcuts import render
# from django import forms

from django.contrib.auth.decorators import login_required
# from datetime import datetime, timedelta, time

# @login_required
from counter.models import Counter
def Index(request):
	# today = datetime.now().date()
	# yesterday = today - timedelta(1)
	# tomorrow = today + timedelta(1)
	# today_start = datetime.combine(today, time())
	# today_end = datetime.combine(tomorrow, time())
	# print(yesterday)
	fname = "index.html"

	c1=''
	c2=''
	c3=''
	c4=''
	c5=''
	c6=''
	c7=''
	c8=''
	c9=''
	c10=''
	c11=''
	c12=''
	# current_job
	counter_list = Counter.objects.filter(
						active=True )
	for c in counter_list:
		if c.counter_number==1 :
			c1 = c.current_job if c.current_job else ''
		if c.counter_number==2 :
			c2 = c.current_job if c.current_job else ''
		if c.counter_number==3 :
			c3 = c.current_job if c.current_job else ''
		if c.counter_number==4 :
			c4 = c.current_job if c.current_job else ''
		if c.counter_number==5 :
			c5 = c.current_job if c.current_job else ''
		if c.counter_number==6 :
			c6 = c.current_job if c.current_job else ''
		if c.counter_number==7 :
			c7 = c.current_job if c.current_job else ''
		if c.counter_number==8 :
			c8 = c.current_job if c.current_job else ''
		if c.counter_number==9 :
			c9 = c.current_job if c.current_job else ''
		if c.counter_number==10 :
			c10 = c.current_job if c.current_job else ''
		if c.counter_number==11 :
			c11 = c.current_job if c.current_job else ''
		if c.counter_number==12 :
			c12 = c.current_job if c.current_job else ''
	# print(c1,c2,c3,c4,c5,c6,sc7,c8,c9,c10,c11,c12)
	return render(
		request,
		fname,
		{

			'c1':c1,'c2':c2,'c3':c3,'c4':c4,'c5':c5,'c6':c6,
			'c7':c7,'c8':c8,'c9':c9,'c10':c10,'c11':c11,'c12':c12
		}
	)
	# return render(request, 'index.html')
#			'object_list' : counter_list,

from django.http import JsonResponse
from django_q.tasks import async_task

def testQView(request):
    json_payload = {
        "message": "Hello world!"
    }
    # enqueue the task
    async_task("job.services.sleep_and_print", 10)
    #
    return JsonResponse(json_payload)
