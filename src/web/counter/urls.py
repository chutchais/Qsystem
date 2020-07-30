from django.contrib import admin
from django.urls import path


from .views import (CounterListView,
					CounterDetailView)

urlpatterns = [
    path('', CounterListView.as_view(), name='list'),
    path('<slug:pk>', CounterDetailView.as_view(), name='detail'),
]