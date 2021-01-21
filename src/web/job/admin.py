from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from datetime import date

# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

from .models import Job,Job_Archive

class JobAdmin(admin.ModelAdmin):
	search_fields       = []
	list_filter         = ['on_process','active','section','counter']
	list_display        = ('queue_number','section','counter','on_process','created_date','started_date','finished_date','active','user')
	readonly_fields     = ['modified_date','created_date','user']
	fieldsets = [
		('Basic Information',{'fields': ['queue_number','section','counter','on_process','note','created_date',('started_date','finished_date','user'),'modified_date','active']}),
	]
admin.site.register(Job,JobAdmin)

# Added on Jan 21,2021 -- TO Archive Job

class JobDateFilter(admin.SimpleListFilter):
	# Human-readable title which will be displayed in the
	# right admin sidebar just above the filter options.
	title = _('Job Created Date Range')

	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'created_date'

	def lookups(self, request, model_admin):
		"""
		Returns a list of tuples. The first element in each
		tuple is the coded value for the option that will
		appear in the URL query. The second element is the
		human-readable name for the option that will appear
		in the right sidebar.
		"""
		return (
			('today', _('Today')),
			('yesterday', _('Yesterday')),
			('thisweek', _('This week')),
			('lastweek', _('Last week')),
			('thismonth', _('This month')),
			('lastmonth', _('Last month')),
		)

	def queryset(self, request, queryset):
		"""
		Returns the filtered queryset based on the value
		provided in the query string and retrievable via
		`self.value()`.
		"""
		# Compare the requested value (either '80s' or '90s')
		# to decide how to filter the queryset.
		import datetime, pytz
		tz 			= pytz.timezone('Asia/Bangkok')
		today_tz 	=   datetime.datetime.now(tz=tz)

		from datetime import date
		if self.value() == 'today':
			today = today_tz#date.today()
			return queryset.filter(created_date__year=today.year,
								created_date__month=today.month,
								created_date__day=today.day).order_by('created_date')

		if self.value() == 'yesterday':
			import datetime
			# today = date.today() - datetime.timedelta(days=1)
			today = today_tz - datetime.timedelta(days=1)
			return queryset.filter(created_date__year=today.year,
								created_date__month=today.month,
								created_date__day=today.day).order_by('created_date')
		
		if self.value() == 'thisweek':
			import datetime
			date = today_tz #datetime.date.today()
			start_week = date - datetime.timedelta(date.weekday())
			end_week = start_week + datetime.timedelta(7)
			return queryset.filter(created_date__range=[start_week, end_week]).order_by('created_date')

		if self.value() == 'lastweek':
			import datetime
			date = today_tz#datetime.date.today()
			date_lastweek = date - datetime.timedelta(days=7)
			start_week = date_lastweek - datetime.timedelta(date_lastweek.weekday())
			end_week = start_week + datetime.timedelta(7)
			print (start_week, end_week)
			# date = end_week + datetime.timedelta(days=1)
			# start_week = date - datetime.timedelta(date.weekday())
			# end_week = start_week + datetime.timedelta(7)
			return queryset.filter(created_date__range=[start_week, end_week]).order_by('created_date')

		if self.value() == 'thismonth':
			today = today_tz #date.today()
			# print('this month')
			return queryset.filter(created_date__year=today.year,
								created_date__month=today.month).order_by('created_date')

		if self.value() == 'lastmonth':
			import datetime
			# today = date.today().replace(day=1) - datetime.timedelta(days=1)
			today = today_tz.replace(day=1) - datetime.timedelta(days=1)
			# print('last month',today)
			return queryset.filter(created_date__year=today.year,
								created_date__month=today.month).order_by('created_date')


class jobResource(resources.ModelResource):
	class Meta:
		model = Job_Archive
		fields = '__all__'

class JobArchiveAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields       = []
	list_filter         = [JobDateFilter,'section','counter']
	list_display        = ('queue_number','section','counter','on_process','created_date','started_date','finished_date','active','user')
	readonly_fields     = ['modified_date','created_date','user']
	fieldsets = [
		('Basic Information',{'fields': ['queue_number','section','counter','on_process','note','created_date',('started_date','finished_date','user'),'modified_date','active']}),
		('Statistic',{'fields': ['year_arch','month_arch','day_created',
								'hour_created','day_completed','hour_completed',
								'waiting_time','process_time','total_time']}),
	]
admin.site.register(Job_Archive,JobArchiveAdmin)
