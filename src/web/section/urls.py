from django.contrib import admin
from django.urls import path


from .views import (SectionListView,
					SectionDetailView,
					create_next_queue)

urlpatterns = [
    path('', SectionListView.as_view(), name='list'),
    path('<slug:pk>', SectionDetailView.as_view(), name='detail'),
    path('<slug:pk>/nextcall', create_next_queue, name='next_queue'),
]