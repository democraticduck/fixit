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

from .forms import LoginForm, SignUpForm
from .models import Report

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

def report(request):
    assert isinstance(request, HttpRequest) #checks if request is an instance of HttpRequest
    return render(
        request,
        'app/report.html',
        {
            'title':'Report',
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
            
        }
    )

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
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