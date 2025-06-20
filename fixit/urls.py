from app import views as main_views
from app.views import Reportlist, ReportDetail, Home, Contact, About, ReportView, Login, Signup, CoordinatorSignup, CoordinatorReportList, CoordinatorReportDetail
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path
from django.conf import settings
from django.contrib.auth.decorators import login_required

admin.autodiscover()
admin.site.site_header = "Fixit Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='def'),
    re_path(r'^home$', Home.as_view(), name='Home'),
    re_path(r'^contact$', Contact.as_view(), name='contact'), #^ means starts with, $ denotes end of string
    re_path(r'^about$', About.as_view(), name='about'),
    re_path(r'^report/$',login_required(ReportView.as_view()),name='report'),
    re_path(r'^login/$',Login.as_view(),name='login'),
    path('signup/', Signup.as_view(), name='signup'),
    path(r'reportlist/', login_required(Reportlist.as_view()), name='reportlist'),
    path(r'reportdetail', login_required(ReportDetail.as_view()), name='reportdetail'),
    re_path(r'^logout$',LogoutView.as_view(template_name = 'app/home.html'),name='logout'),
    path('coordinator/signup/', CoordinatorSignup.as_view(), name='coordinator_signup'),
    path('coordinator/reportlist/', login_required(CoordinatorReportList.as_view()), name='coordinator_reportlist'),
    path('coordinator/reportdetail', login_required(CoordinatorReportDetail.as_view()), name='coordinator_reportdetail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
