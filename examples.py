from django.views.generic import ListView
from .models import Report
from abc import ABC, abstractmethod
from django.http import HttpResponse
#get method returns a HttpResponse
class ReportListView(ListView):
    model = Report
    template_name = 'list.html'

#interface for decorator
class BaseViewDecorator(ABC):
    def __init__(self, view_fc):
        self.view_fc = view_fc

    #mimic as if decorator is view fc, thus callable
    def __call__(self, request, *args, **kwargs):
        self.view_fc(self, request, *args, **kwargs)

    #to delegate all attr calls to viewfc
    def __getattr__(self, key):
        return getattr(self.view_fc, key)

#concrete decorator for authentication check
class LoginRequiredDecorator(BaseViewDecorator):
    def __call__(self, request, *args, **kwargs):
        #check if user is authenticated
        if not request.user.is_authenticated:
            return HttpResponse("unauthorised", status=401)

        return super().__call__(self, request, *args, **kwargs)

class UserPrivilegeDecorator(BaseViewDecorator):
    def __call__(self, request, *args, **kwargs):
        #check if user is admin
        if not request.user.is_admin:
            return HttpResponse("unauthorised", status=401)

        return super().__call__(self, request, *args, **kwargs)

class RequireHttpMethodsDecorator(BaseViewDecorator):
    def __init__(self, methods):
        super().__init__
        self.methods = methods

    def __call__(self, request, *args, **kwargs):
        #check if request has correct method
        if request.method not in methods:
            return HttpResponse("Invalid method", status=405)

        return super().__call__(self, request, *args, **kwargs)