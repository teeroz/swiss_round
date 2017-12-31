"""GenGoZ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import login, password_change, logout, password_change_done
from django.urls import re_path, include

urlpatterns = [
    re_path(r'^exams/', include('exams.urls')),
    re_path(r'^swiss/', include('swiss.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^login$', login, {'template_name': 'admin/login.html'}, name='login'),
    re_path(r'^logout$', logout, {'next_page': '/exams/1/w'}, name='logout'),
    re_path(r'^password_change$', password_change,
            {'template_name': 'registration/password_change_form.html'}, name='password_change'),
    re_path(r'^password_change_done$', password_change_done,
            {'template_name': 'registration/password_change_done.html'}, name='password_change_done'),
]
