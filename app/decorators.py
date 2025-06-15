from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from .models import BaseUser



def isRoleFact(
    role,
):  
    def is_role(user):
        return isinstance(user, BaseUser) and user.role == role

    return isRole

def admin_only(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    actual_decorator = user_passes_test(
        isRoleFact(BaseUser.USER_ROLE.ADMIN),
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def coord_only(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    actual_decorator = user_passes_test(
        isRoleFact(BaseUser.USER_ROLE.COORDINATOR),
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    if function:
        return actual_decorator(function)
    return actual_decorator