"""qsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from .views import Index

urlpatterns = [
	path('', Index),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('section/',include(('section.urls','section'),namespace='section')),
    path('counter/',include(('counter.urls','counter'),namespace='counter')),
    path('job/',include(('job.urls','job'),namespace='job')),
    # path('signup/', views.signup, name='signup'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib import admin
admin.site.site_header = 'LCB1 Q-System'
admin.site.site_title = 'LCB1 Q-System'


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns