from django.contrib import admin
from django.urls import path


from .views import (JobListView,
					JobDetailView,JobDeleteView,
					assign_counter,
					cancel_job,complete_job,call_job,
                    JobDayArchiveView)

urlpatterns = [
    path('', JobListView.as_view(), name='list'),
    path('<slug:pk>', JobDetailView.as_view(), name='detail'),
    path('<slug:pk>/delete', JobDeleteView.as_view(), name='delete'),
    path('<slug:job_pk>/calljob',call_job, name='calljob'),
    path('<slug:job_pk>/assign/<slug:counter_pk>',assign_counter, name='assign'),
    path('<slug:job_pk>/cancel',cancel_job, name='cancel'),
    path('<slug:job_pk>/complete',complete_job, name='complete'),
    path('archive/<int:year>/<str:month>/<int:day>/',
         JobDayArchiveView.as_view(),
         name="archive_day"),
]