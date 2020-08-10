from django.contrib import admin

# Register your models here.

from .models import Section

class SectionAdmin(admin.ModelAdmin):
    search_fields       = ['name','description']
    list_filter         = []
    list_display        = ('name','seq','description','prefix','starting_number','maximum_number','current_number','color','modified_date')
    readonly_fields     = ['modified_date','created_date']
    fieldsets = [
        ('Basic Information',{'fields': ['name','seq','color','description','prefix','starting_number','maximum_number','current_number','modified_date']}),
    ]
admin.site.register(Section,SectionAdmin)
