from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import uuid

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, ic_num, password=None, **extra_fields):
        if not ic_num:
            raise ValueError('The IC number must be set')
        user = self.model(ic_num=ic_num, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, ic_num, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ad')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(ic_num, password, **extra_fields)


class USER_ROLE(models.TextChoices):
    ADMIN = 'ad', _('Admin')
    COORDINATOR = 'co', _('Coordinator')
    CUSTOMER = 'cu', _('Customer')


class User(AbstractUser):
    ic_num = models.CharField(max_length=12, unique=True, primary_key=True)
    phone_num = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(choices = USER_ROLE.choices, default=USER_ROLE.CUSTOMER, max_length=2)
    username = None  # We disable username
    USERNAME_FIELD = 'ic_num'
    REQUIRED_FIELDS = []  # No other required fields

    objects = UserManager()  # <-- add this line


class RegistrationRequest(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    ic_num = models.CharField(max_length=12, unique=True)
    phone_num = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Hashed password
    date_requested = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.ic_num})"


class Report(models.Model):
    class CASE_STATUS(models.TextChoices):
        PENDING = 'pe', _('Pending')
        OPEN = 'op', _('Open')
        IN_PROGRESS = 'ip', _('In Progress')
        CLOSED = 'cl', _('Closed')

    class APPROVE_STATUS(models.TextChoices):
        APPROVED = 'ap', _('Approved')
        REJECTED = 'rj', _('Rejected')
        PENDING = 'pe', _('Pending')

    class CATEGORY(models.TextChoices):
        TRANSPORT = 'tr', _('Transport')
        ENVIRONMENT = 'en', _('Environment')
        INFRASTRUCTURE = 'in', _('Infrastructure')
        OTHER = 'ot', _('Other')

    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    title = models.TextField(null=False, blank=False, max_length=50)
    description = models.TextField(null=True,default=None, blank=True, max_length=500)
    loc_lng = models.DecimalField(null=False, default=None, blank=False, max_digits=9, decimal_places=6)
    loc_lat = models.DecimalField(null=False, default=None, blank=False, max_digits=9, decimal_places=6)
    approve_status = models.CharField(choices = APPROVE_STATUS.choices, default=APPROVE_STATUS.PENDING, max_length=2)
    case_status = models.CharField(choices = CASE_STATUS.choices, default=CASE_STATUS.PENDING, max_length=2)
    progress_detail = models.TextField(null=True, blank=True, max_length=500)
    category = models.CharField(choices = CATEGORY.choices, default=CATEGORY.OTHER, max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo_url = models.TextField(null=True, blank=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_reports') #related name for related obj back to current
    manage_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='managed_reports', limit_choices_to={ 'role': USER_ROLE.COORDINATOR })

    def __str__(self):
        return str(self.title)
    
    @property
    def days_since_creation(self):
        diff = timezone.now() - self.created_at
        return diff.days


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    title = models.TextField(null=True, default=None, blank=True, max_length=60)
    description = models.TextField(null=True, default=None, blank=True, max_length=200)
    sent_at = models.DateTimeField(default=timezone.now)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='notifications')

    def get_report_title(self):
        return self.report.title
    
    def __str__(self):
        return str(self.id)
