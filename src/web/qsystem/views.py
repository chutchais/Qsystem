from django.shortcuts import render
from django import forms

from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, time

# @login_required
from counter.models import Counter
def Index(request):
	today = datetime.now().date()
	yesterday = today - timedelta(1)
	tomorrow = today + timedelta(1)
	today_start = datetime.combine(today, time())
	today_end = datetime.combine(tomorrow, time())
	print(yesterday)
	fname = "index.html"
	counter_list = Counter.objects.filter(
						active=True ).order_by('counter_number')

	
	return render(
		request,
		fname,
		{
			'object_list' : counter_list
		}
	)
	# return render(request, 'index.html')