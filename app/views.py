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

from django.contrib.auth.decorators import login_required
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
            'app/index.html',
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
        {
            'title':'ABC System',
            'message':'This application processes ...',
            'year':datetime.now().year,
        }
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
            obj.user_id = request.user 
            obj.photo_url = dir_path
            obj.save()
            
    
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

class Reportlist(View):
    def get(self, request):
        reports = Report.objects.all()
        return render(request, "app/reportlist.html", {"reports": reports})






