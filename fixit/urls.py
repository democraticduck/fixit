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
from app import views as main_views
from app.views import Reportlist, ReportDetail
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

admin.autodiscover()
admin.site.site_header = "Fixit Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('newindex/', main_views.newindex, name='newindex'),
    re_path(r'^$', main_views.home, name='home'),
    re_path(r'^contact$', main_views.contact, name='contact'), #^ means starts with, $ denotes end of string
    re_path(r'^about$', main_views.about, name='about'),
    path('login/',
        main_views.login_user,
        name='login'),
    re_path(r'^signup/$',
        main_views.signup,
        name='signup'),
    re_path(r'^report/$',
        main_views.report,
        name='report'),
    path(r'reportlist/', Reportlist.as_view(), name='reportlist'),
    path(r'detail/', ReportDetail.as_view(), name='reportdetail'),
    re_path(r'^logout$',
        LogoutView.as_view(template_name = 'app/index.html'),
        name='logout'),
    re_path(r'^menu$', main_views.menu, name='menu'),
    path('coordinator/menu/', main_views.coordinator_menu, name='coordinator_menu'),
    path('coordinator/signup/', main_views.coordinator_signup, name='coordinator_signup'),
    path('coordinator/reportlist/', main_views.coordinator_reportlist, name='coordinator_reportlist'),
    path('coordinator/reportdetail/', main_views.coordinator_reportdetail, name='coordinator_reportdetail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
