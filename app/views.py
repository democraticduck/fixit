from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from datetime import datetime
from django.contrib import messages
from django.views import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseNotFound

import shortuuid
from .forms import LoginForm, SignUpForm, ReportForm
from .models import Report
from django.conf import settings

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return(redirect('/menu'))
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


def menu(request):
    #if user
    check_employee = request.user.groups.filter(name='employee').exists()

    context = {
            'title':'Main Menu',
            'is_employee': check_employee,
            'year':datetime.now().year,
        }
    context['user'] = request.user

    return render(request,'app/menu.html',context)

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
        return(redirect('/menu'))
    if request.method == 'POST':
        if not ic.isdigit() or password == '':
            messages.info(request, ('Invalid field(s)')) #add to html
            return redirect('/login')       

        user = authenticate(request, username=ic, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, ('Successfully login!'))
            return redirect('/menu')

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
            return redirect('home')

    else:
        form = SignUpForm()
    context = {'form' : form}
    return render(request, 'app/signup.html' , context)

def Home(request):
    return render(request, 'app/home.html')

class Reportlist(View):
    def get(self, request):
        reports = Report.objects.filter(user_id=request.user)
        
        return render(request, "app/reportlist.html", {"reports": reports})


class ReportDetail(View):
    def get(self, request):
        id = request.GET.get('id')
        
        reports = Report.objects.filter(id=id).values()
        report = list(reports)[0]
        #import re
        import os
        #idWoDashes = re.sub(r"-", "", id) 
        img_name = os.listdir(str(settings.MEDIA_ROOT) + "/" + report['photo_url'])
        img_path_list = [settings.MEDIA_URL + report['photo_url'] + "/" + name for name in img_name]
        
        return render(request, "app/reportdetail.html", {"report": report, "img_path_list": img_path_list, "fields": {
            "ID": report['id'],
            "Title": report['title'],
            "Description": report['description'],
            "Status": Report.STATUS(report['status']).label,
            "Category": Report.CATEGORY(report['category']).label,
            "Created at": report['created_at'],
        }
        })

def coordinator_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            ic = form.cleaned_data['ic_num']
            pwd = form.cleaned_data['password']
            user = authenticate(request, ic_num=ic, password=pwd)
            if user:
                login(request, user)
                return redirect('view_reports')
    else:
        form = LoginForm()
    return render(request, 'app/coordinator_login.html', {'form': form})

def coordinator_register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coordinator_login')
    else:
        form = SignUpForm()
    return render(request, 'app/coordinator_register.html', {'form': form})

@login_required
def coordinator_view_reports(request):
        reports = Report.objects.all()
        
        return render(request, "app/coordinator_view_reports.html", {"reports": reports})

@login_required
def coordinator_update_status(request, report_id):
    reports = Report.objects.filter(id=report_id).values()
    if not reports:
        return HttpResponseNotFound("Report not found.")

    report = list(reports)[0]

    import os
    img_path = os.path.join(settings.MEDIA_ROOT, report['photo_url'])
    img_name = os.listdir(img_path) if os.path.exists(img_path) else []
    img_path_list = [settings.MEDIA_URL + report['photo_url'] + "/" + name for name in img_name]

    return render(request, "app/coordinator_update_status.html", {
        "report": report,
        "img_path_list": img_path_list,
        "fields": {
            "ID": report['id'],
            "Title": report['title'],
            "Description": report['description'],
            "Status": Report.STATUS(report['status']).label,
            "Category": Report.CATEGORY(report['category']).label,
            "Created at": report['created_at'],
        }
    })



