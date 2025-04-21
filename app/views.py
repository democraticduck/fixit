from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from datetime import datetime

from django.contrib.auth.decorators import login_required

from .forms import LoginForm, SignUpForm

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

@login_required
def menu(request):
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

def login(request):
    """Renders the login page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return(redirect('/menu'))
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST) #populate form with data from request.POST
        if form.is_valid():
            # Perform login logic here
            return redirect('/menu')
    
    form = SignupForm() #new form instance
    return render(
        request,
        'app/login.html',
        {
            'title':'Login',
            'form': form, #if invalid form, return bound form with errors, else return new form
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
    return render(request, 'signup.html' , context)