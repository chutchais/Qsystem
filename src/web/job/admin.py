from django.contrib import admin

# Register your models here.

from .models import Job

class JobAdmin(admin.ModelAdmin):
    search_fields       = []
    list_filter         = ['on_process','active','section','counter']
    list_display        = ('queue_number','section','counter','on_process','created_date','started_date','finished_date','active')
    readonly_fields     = ['modified_date','created_date']
    fieldsets = [
        ('Basic Information',{'fields': ['queue_number','section','counter','on_process','note','created_date',('started_date','finished_date'),'modified_date','active']}),
    ]
admin.site.register(Job,JobAdmin)
