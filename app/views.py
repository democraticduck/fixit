from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from .forms import LoginForm, SignUpForm, ReportForm, ReportUpdateForm
from .models import Notification, Report

import shortuuid, os

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return(redirect('/home'))
    else:
        return render(
            request,
            'app/home.html',
            {
                'title':'Home Page',
                'year': datetime.now().year,
            }
        )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Dr. Yeoh.',
            'year':datetime.now().year,
        }
    )


def about(request):

    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
    )


def handle_upload(f, dir_path, name):
    import pathlib
    pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True) 
    path = dir_path + "/" + name
    with open(path, "wb+") as destination:
        print('path is ' , path)
        for chunk in f.chunks():
            destination.write(chunk)
    
    print('success')


@login_required(login_url='/login')
def report(request):
    assert isinstance(request, HttpRequest) #checks if request is an instance of HttpRequest
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


def newindex(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/newindex.html',
        {
            'title':'New Index',
        }
    )


def onlyInt(val):
        if not val.isdigit():
            raise ValidationError('ID contains characters')


def login_user(request):
    """Renders the login page."""
    assert isinstance(request, HttpRequest)
    
    ic = request.POST.get('ic_num')
    password = request.POST.get('password')
    print(ic)
    if request.user.is_authenticated:
        if request.user.role == 'cu':
            return(redirect('/home'))
        else:
            return(redirect('/home'))
    if request.method == 'POST':
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


def Home(request):
    return render(request, 'app/home.html')


class Reportlist(View):
    def get(self, request):
        reports = request.user.submitted_reports.all()
        return render(request, "app/reportlist.html", {"reports": reports})


class ReportDetail(View):
    def get(self, request):
        id = request.GET.get('id')
        
        reports = Report.objects.filter(id=id).values()
        report = list(reports)[0]
        import os
        #idWoDashes = re.sub(r"-", "", id) 
        img_name = os.listdir(str(settings.MEDIA_ROOT) + "/" + report['photo_url'])
        img_path_list = [settings.MEDIA_URL + report['photo_url'] + "/" + name for name in img_name]
        
        return render(request, "app/reportdetail.html", {"report": report, "img_path_list": img_path_list, "fields": {
            "ID": report['id'],
            "Title": report['title'],
            "Description": report['description'],
            "Category": Report.CATEGORY(report['category']).label,
            "Created at": report['created_at'],
            "Approve Status": Report.APPROVE_STATUS(report['approve_status']).label,
            "Case Status": Report.CASE_STATUS(report['case_status']).label,
            "Progress Detail": report['progress_detail'],
        }})


def coordinator_signup(request):
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
        form.fields['role'].initial = 'co'
    return render(request, 'app/coordinator_signup.html', {'form': form})


@login_required
def coordinator_reportlist(request):
    reports = request.user.managed_reports.all()
    return render(request, "app/coordinator_reportlist.html", {'reports': reports})


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
            return redirect('/home')
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
