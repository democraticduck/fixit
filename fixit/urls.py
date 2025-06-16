from app import views as main_views
from app.views import Reportlist, ReportDetail
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path
from django.conf import settings

admin.autodiscover()
admin.site.site_header = "Fixit Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('newindex/', main_views.newindex, name='newindex'),
    re_path(r'^$', main_views.home, name='home'),
    re_path(r'^home$', main_views.Home, name='Home'),
    re_path(r'^contact$', main_views.contact, name='contact'), #^ means starts with, $ denotes end of string
    re_path(r'^about$', main_views.about, name='about'),
    re_path(r'^login/$',main_views.login_user,name='login'),
    path('signup/', main_views.signup, name='signup'),
    re_path(r'^report/$',main_views.report,name='report'),
    path(r'reportlist/', Reportlist.as_view(), name='reportlist'),
    path(r'reportdetail', ReportDetail.as_view(), name='reportdetail'),
    re_path(r'^logout$',LogoutView.as_view(template_name = 'app/home.html'),name='logout'),
    path('coordinator/signup/', main_views.coordinator_signup, name='coordinator_signup'),
    path('coordinator/reportlist/', main_views.coordinator_reportlist, name='coordinator_reportlist'),
    path('coordinator/reportdetail', main_views.coordinator_reportdetail, name='coordinator_reportdetail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
