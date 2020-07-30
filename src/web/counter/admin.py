from django.contrib import admin

# Register your models here.
from .models import Counter

class CounterAdmin(admin.ModelAdmin):
    search_fields       = ['name','description']
    list_filter         = []
    list_display        = ('name','counter_number','description','modified_date')
    readonly_fields     = ['modified_date','created_date']
    fieldsets = [
        ('Basic Information',{'fields': ['name','counter_number','description','modified_date']}),
    ]
admin.site.register(Counter,CounterAdmin)