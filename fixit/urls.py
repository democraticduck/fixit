"""fixit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path
from app import views as main_views
import django.contrib.auth.views
from django.contrib.auth.views import LoginView, LogoutView
from datetime import datetime
from django.views.generic import TemplateView  
from app.views import Reportlist, ReportDetail
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('newindex/', main_views.newindex, name='newindex'),
    re_path(r'^$', main_views.home, name='home'),
    re_path(r'^contact$', main_views.contact, name='contact'), #^ means starts with, $ denotes end of string
    re_path(r'^about$', main_views.about, name='about'),
    re_path(r'^login/$',
        main_views.login_user,
        name='login'),
    re_path(r'^signup/$',
        main_views.signup,
        name='signup'),
    re_path(r'^report/$',
        LoginView.as_view(template_name = 'app/report.html'),
        name='report'),
    re_path(r'reportlist/', Reportlist.as_view(), name='reportlist'),
    re_path(r'detail/', ReportDetail.as_view(), name='reportdetail'),
    re_path(r'^logout$',
        LogoutView.as_view(template_name = 'app/index.html'),
        name='logout'),
    re_path(r'^menu$', main_views.menu, name='menu'),
] + static(settings.STATIC_URL)
