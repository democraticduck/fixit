from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from .models import User, USER_ROLE
from django.urls import reverse_lazy


def isRoleFact(
    role,
):  
    def is_role(user):
        return isinstance(user, User) and user.role == role

    return is_role

def admin_only(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    if login_url is None:
        login_url = reverse_lazy('Home')

    actual_decorator = user_passes_test(
        isRoleFact(USER_ROLE.ADMIN),
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def coord_only(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    if login_url is None:
        login_url = reverse_lazy('Home')

    actual_decorator = user_passes_test(
        isRoleFact(USER_ROLE.COORDINATOR),
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    if function:
        return actual_decorator(function)
    return actual_decorator