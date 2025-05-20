from django.views.generic import ListView
from .models import Report
from abc import ABC, abstractmethod
from django.http import HttpResponse
#get method returns a HttpResponse
class ReportListView(ListView):
    model = Report
    template_name = 'list.html'

class ViewFunction(ABC):
    #define interface for view function
    #make sure view function is callable
    @abstractmethod
    def __call__(self, request, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def view_class(self):
        pass
    
    @property
    @abstractmethod
    def view_initkwargs(self):
        pass

    @property
    @abstractmethod
    def __doc__(self):
        pass

    @property
    @abstractmethod
    def __module__(self):
        pass

    @property
    @abstractmethod
    def __annotations__(self):
        pass


#interface for decorator
class BaseViewDecorator(ABC):
    def __init__(self, view_fc: ViewFunction):
        self.view_fc = view_fc

    #mimic as if decorator is view fc, thus callable
    def __call__(self, request, *args, **kwargs):
        self.view_fc(request, *args, **kwargs)

    #to delegate all attr calls to viewfc
    def __getattr__(self, key):
        return getattr(self.view_fc, key)

#concrete decorator for authentication check
class LoginRequiredDecorator(BaseViewDecorator):
    def __call__(self, request, *args, **kwargs):
        #check if user is authenticated
        if not request.user.is_authenticated:
            return HttpResponse("unauthorised", status=401)

        return super().__call__(request, *args, **kwargs)

class UserPrivilegeDecorator(BaseViewDecorator):
    def __call__(self, request, *args, **kwargs):
        #check if user is admin
        if not request.user.is_admin:
            return HttpResponse("unauthorised", status=401)

        return super().__call__(request, *args, **kwargs)

class RequireHttpMethodsDecorator(BaseViewDecorator):
    def __init__(self, view_fc, methods):
        super().__init__(view_fc)
        self.methods = methods

    def __call__(self, request, *args, **kwargs):
        #check if request has correct method
        if request.method not in self.methods:
            return HttpResponse("Invalid method", status=405)

        return super().__call__(request, *args, **kwargs)

#urls.py
from .views import ReportListView, LoginRequiredDecorator, UserPrivilegeDecorator, RequireHttpMethodsDecorator
#usage example:
decorated_view = RequireHttpMethodsDecorator(LoginRequiredDecorator(ReportListView.as_view()), methods=['GET'])



#template method:
from django.field import _clean_bound_field
from django import forms
from django.utils.translation import gettext_lazy as _
class BaseFormView:
    def __init__(self):
        self.base_fields = {}

    def _clean_fields(self):
        #loop through all fields in form
        for name, bf in self.base_fields:
            field = bf.field
            self.cleaned_data[name] = field._clean_bound_field(bf)

    #custom hook
    def _post_clean(self):
        #custom logic to override in subclasses optionally
        pass 

    def full_clean(self):
        #template method
        #clean all field values
        self._clean_fields()
        self._post_clean()

class ReportForm(BaseFormView):
    self.base_fields = {
        title = forms.CharField()
        description = forms.CharField()
        category = forms.CharField()
    }
    def _post_clean(self):
        #gets called part of BaseFormView's full_clean
        #clean value for some fields
        self.cleaned_data['title'].strip()
        self.description['description'].strip()

class LoginForm(BaseFormView):
    self.base_fields = {
        id = forms.CharField()
        password = forms.CharField(widget = forms.PasswordInput)
    }
    def _post_clean(self):
        #gets called part of BaseFormView's full_clean
        #clean value for some fields
        self.cleaned_data['id'].strip()

#views.py
from .forms import ReportForm
#usage example:
def report(request):
    return render(
        request,
        'app/report.html',
        {
            'form': ReportForm,
        }
    )



#strategy pattern:
from abc import ABC, abstractmethod
import re
class Validator(ABC):
    @abstractmethod
    
    def execute(data):
        pass

class PasswordValidator(Validator):
    #make sure password more than 8 characters
    def execute(data):
        return 8 < len(data)

class EmailValidator(Validator):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    #validate email format
    
    def execute(data):
        return bool(re.fullmatch(regex, data))

class ICValidator(Validator):
    regex = r'^[0-9]{12}$'
    #validate ic format
    
    def execute(data):
        return bool(re.fullmatch(regex, data))

class Input:
    def __init__(self, validator=None):
        self.validator = validator

    def set_validator(self, validator):
        self.validator = validator
    
    def validate(self, data):
        if self.validator is not None:
            return self.validator.execute(data)
        return False

class PasswordInput(Input):
    def __init__(self):
        super().__init__(PasswordValidator())

class EmailInput(Input):
    def __init__(self):
        super().__init__(EmailValidator())

class ICInput(Input):
    def __init__(self):
        super().__init__(ICValidator())