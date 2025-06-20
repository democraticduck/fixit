from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login

from django.contrib.auth.hashers import make_password
from django.forms import ValidationError
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from .forms import LoginForm, SignUpForm, ReportForm, ReportUpdateForm, RegistrationForm
from .models import Notification, Report, RegistrationRequest

import shortuuid, os


from django.views import View
from django.http import HttpResponse
from django.shortcuts import render



class BaseView(View):
    template_name = None
    request = None

    def get(self, request, *args, **kwargs):
        assert isinstance(request, HttpRequest)
        self.request = request
        context = self.get_context_data(**kwargs)
        return self.get_render_to_response(context)

    def post(self, request, *args, **kwargs):
        assert isinstance(request, HttpRequest)
        self.request = request
        context = self.post_context_data(**kwargs)
        return self.post_render_to_response(context)

    def get_context_data(self, **kwargs):
        return {}
    
    def post_context_data(self, **kwargs):
        return {}

    def get_render_to_response(self, context):
        if not self.template_name:
            return HttpResponse("No template_name defined", status=500)
        return render(self.request, self.template_name, context)
    
    def post_render_to_response(self, context):
        return self.get_render_to_response(context)



class Home(BaseView):
    template_name = 'app/home.html'
    


class Contact(BaseView):
    template_name = 'app/contact.html'


class About(BaseView):
    template_name = 'app/about.html'


def handle_upload(f, dir_path, name):
    import pathlib
    pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True) 
    path = dir_path + "/" + name
    with open(path, "wb+") as destination:
        print('path is ' , path)
        for chunk in f.chunks():
            destination.write(chunk)
    
    print('success')


class ReportView(BaseView):
    template_name = 'app/report.html'

    def get_context_data(self, **kwargs):
        return {
            'title':'Report',
            'form': ReportForm()
        }

    def post_render_to_response(self, context):
        request = self.request
        if request.method == 'POST':
            form = ReportForm(request.POST)
            if form.is_valid():
                dir_name = shortuuid.uuid() #generate uuid for folder in media
                dir_path = str(settings.MEDIA_ROOT) + "/" + dir_name

                for value in request:
                    print(value)

                for idx, f in enumerate(request.FILES.getlist("photo")):
                    handle_upload(f, dir_path, str(f.name))

                obj = form.save(commit=False)
                obj.loc_lat = request.POST.get('loc_lat')
                obj.loc_lng = request.POST.get('loc_lng')
                obj.user_id = request.user
                obj.photo_url = dir_name #save as name of dir
                obj.save()
                messages.success(request, ('Success!'))
                return redirect('/reportlist')
            
            else:
                messages.success(request, ('Please fill in required fields'))
                return redirect('/report')

"""
@login_required(login_url='/login')
def report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            dir_name = shortuuid.uuid() #generate uuid for folder in media
            dir_path = str(settings.MEDIA_ROOT) + "/" + dir_name

            for value in request:
                print(value)

            for idx, f in enumerate(request.FILES.getlist("photo")):
                handle_upload(f, dir_path, str(f.name))

            obj = form.save(commit=False)
            obj.loc_lat = request.POST.get('loc_lat')
            obj.loc_lng = request.POST.get('loc_lng')
            obj.user_id = request.user
            obj.photo_url = dir_name #save as name of dir
            obj.save()
            messages.success(request, ('Success!'))
            return redirect('/reportlist')
        
        else:
            messages.success(request, ('Please fill in required fields'))
            return redirect('/report')
    
    return render(
        request,
        'app/report.html',
        {
            'title':'Report',
            'form': ReportForm()
        }
    )
"""
class Login(BaseView):
    template_name = 'app/login.html'
    def get_context_data(self, **kwargs):
        return {
            'form': LoginForm()
        }
    def post_render_to_response(self, context):
        request = self.request
        ic = request.POST.get('ic_num')
        password = request.POST.get('password')
        print(ic)
        if request.user.is_authenticated:
            if request.user.role == 'cu':
                return(redirect('/home'))
            else:
                return(redirect('/home'))
        if not ic.isdigit() or password == '':
            messages.info(request, ('Invalid field(s)')) #add to html
            return redirect('/login')       

        user = authenticate(request, username=ic, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, ('Successfully login!'))
            if request.user.role == 'cu':
                return(redirect('/home'))
            else:
                return(redirect('/home'))

        messages.success(request, ('Invalid ic or password'))
        return redirect('/login')

"""
def login_user(request): 
    if request.method == 'POST':
        ic = request.POST.get('ic_num')
        password = request.POST.get('password')
        print(ic)
        if request.user.is_authenticated:
            if request.user.role == 'cu':
                return(redirect('/home'))
            else:
                return(redirect('/home'))
        if not ic.isdigit() or password == '':
            messages.info(request, ('Invalid field(s)')) #add to html
            return redirect('/login')       

        user = authenticate(request, username=ic, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, ('Successfully login!'))
            if request.user.role == 'cu':
                return(redirect('/home'))
            else:
                return(redirect('/home'))

        messages.success(request, ('Invalid ic or password'))
        return redirect('/login')
    
    return render(
        request,
        'app/login.html',
        {
            'form': LoginForm()
        }
    )
"""
class Signup(BaseView):
    template_name = 'app/signup.html'
    def get_context_data(self, **kwargs):
        return {
            'form': SignUpForm()
        }
    def post_render_to_response(self, context):
        request = self.request
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['ic_num']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Successfully registered!'))
            return redirect('/home')

"""
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['ic_num']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Successfully registered!'))
            return redirect('/home')
    else:
        form = SignUpForm()
    return render(request, 'app/signup.html' ,{'form' : form})

"""


class Reportlist(BaseView):
    template_name = 'app/reportlist.html'
    def get_context_data(self, **kwargs):
        request = self.request
        reports = self.request.user.submitted_reports.all()
        return {"reports": reports}
        


class ReportDetail(BaseView):
    template_name = 'app/reportdetail.html'

    def get_context_data(self, **kwargs):
        request = self.request
        id = request.GET.get('id')
        
        reports = Report.objects.filter(id=id).values()
        report = list(reports)[0]
        import os
        #idWoDashes = re.sub(r"-", "", id) 
        img_name = os.listdir(str(settings.MEDIA_ROOT) + "/" + report['photo_url'])
        img_path_list = [settings.MEDIA_URL + report['photo_url'] + "/" + name for name in img_name]
        
        return {"report": report, "img_path_list": img_path_list, "fields": {
            "ID": report['id'],
            "Title": report['title'],
            "Description": report['description'],
            "Category": Report.CATEGORY(report['category']).label,
            "Created at": report['created_at'],
            "Approve Status": Report.APPROVE_STATUS(report['approve_status']).label,
            "Case Status": Report.CASE_STATUS(report['case_status']).label,
            "Progress Detail": report['progress_detail'],
        }}

class CoordinatorSignup(BaseView):
    template_name = 'app/coordinator_signup.html'

    def get_context_data(self, **kwargs):
        return {
            'form': RegistrationForm()
        }

    def post_render_to_response(self, context):
        request = self.request
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            RegistrationRequest.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                ic_num=data['ic_num'],
                phone_num=data['phone_num'],
                email=data['email'],
                password=make_password(data['password1']),
            )
            messages.success(request, "Registration submitted. Please wait for admin approval.")
            return redirect('/home')


"""
def coordinator_signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            RegistrationRequest.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                ic_num=data['ic_num'],
                phone_num=data['phone_num'],
                email=data['email'],
                password=make_password(data['password1']),
            )
            messages.success(request, "Registration submitted. Please wait for admin approval.")
            return redirect('/home')
    else:
        form = RegistrationForm()
    return render(request, 'app/coordinator_signup.html', {'form': form})
"""

class CoordinatorReportList(BaseView):
    template_name = 'app/coordinator_reportlist.html'

    def get_context_data(self, **kwargs):
        request = self.request
        reports = self.request.user.managed_reports.all()
        return {'reports': reports}

"""

@login_required
def coordinator_reportlist(request):
    reports = request.user.managed_reports.all()
    return render(request, "app/coordinator_reportlist.html", {'reports': reports})

"""

class CoordinatorReportDetail(BaseView):
    template_name = 'app/coordinator_reportdetail.html'

    def get_context_data(self, **kwargs):
        request = self.request
        report_id = request.GET.get('id')
        report = get_object_or_404(Report, id=report_id, manage_by=request.user)

        img_path = os.path.join(settings.MEDIA_ROOT, report.photo_url)
        img_name = os.listdir(img_path) if os.path.exists(img_path) else []
        img_path_list = [settings.MEDIA_URL + report.photo_url + "/" + name for name in img_name]

        fields = {
            "ID": report.id,
            "Title": report.title,
            "Description": report.description,
            "Category": Report.CATEGORY(report.category).label,
            "Created at": report.created_at,
            "Approve Status": Report.APPROVE_STATUS(report.approve_status).label,
        }
        if request.method == 'POST':
            form = ReportUpdateForm(request.POST, instance=report)
        else:   
            form = ReportUpdateForm(instance=report)
        
        return {
            "report": report,
            "img_path_list": img_path_list,
            "fields": fields,
            "form": form,
        }

    def post_render_to_response(self, context):
        request = self.request
        report = context['report']
        form = context['form']

        if form.is_valid():
            form.save()
            messages.success(request, "Report updated.")
            Notification.objects.create(
                title=f"Update: {report.title}",
                description="The status of your report has been updated. Please check for details.",
                sent_at=timezone.now(),
                report=report
            )
            return redirect('/coordinator/reportlist')
        
        return render(request, self.template_name, context)

"""
@login_required
def coordinator_reportdetail(request):
    report_id = request.GET.get('id')
    report = get_object_or_404(Report, id=report_id, manage_by=request.user)

    if request.method == 'POST':
        form = ReportUpdateForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, "Report updated.")
            Notification.objects.create(
                title=f"Update: {report.title}",
                description="The status of your report has been updated. Please check for details.",
                sent_at=timezone.now(),
                report=report
            )
            return redirect('/coordinator/reportlist')
    else:
        form = ReportUpdateForm(instance=report)

    img_path = os.path.join(settings.MEDIA_ROOT, report.photo_url)
    img_name = os.listdir(img_path) if os.path.exists(img_path) else []
    img_path_list = [settings.MEDIA_URL + report.photo_url + "/" + name for name in img_name]

    fields = {
        "ID": report.id,
        "Title": report.title,
        "Description": report.description,
        "Category": Report.CATEGORY(report.category).label,
        "Created at": report.created_at,
        "Approve Status": Report.APPROVE_STATUS(report.approve_status).label,
    }

    return render(request, "app/coordinator_reportdetail.html", {
        "report": report,
        "img_path_list": img_path_list,
        "fields": fields,
        "form": form,
    })
"""