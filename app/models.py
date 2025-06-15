from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import uuid

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, ic_num, password, **extra_fields):
        if not ic_num or not password:
            raise ValueError(_('The IC number or password must be set'))
        user = self.model(ic_num=ic_num, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, ic_num, password=None, **extra_fields):
        extra_fields.setdefault('role', 'ad')
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get('role') != 'ad':
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(ic_num, password, **extra_fields)


class BaseUser(AbstractUser):
    class USER_ROLE(models.TextChoices):
        ADMIN = 'ad', _('Admin')
        COORDINATOR = 'co', _('Coordinator')
        CUSTOMER = 'cu', _('Customer')

    class ACCOUNT_STATUS(models.TextChoices):
        ACTIVE = 'ac', _('Active')
        BANNED = 'bn', _('Banned')

    ic_num = models.CharField(max_length=12, null=True, blank=True, unique=True)
    username = None  #Disable username
    
    phone_num = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(choices = USER_ROLE.choices, max_length=2)
    status = models.CharField(choices = ACCOUNT_STATUS.choices, default=ACCOUNT_STATUS.ACTIVE)
    USERNAME_FIELD = 'ic_num' #new username field
    REQUIRED_FIELDS = []  #Remove requried fields

    objects = UserManager()  
    
    def __str__(self):
        return self.ic_num


class Admin(BaseUser):
    work_id = models.CharField(max_length = 255, blank=False)

    def save(self, *args, **kwargs):
        self.role = self.USER_ROLE.ADMIN
        super().save(*args, **kwargs)


class STATES(models.TextChoices):
    JOHOR = 'Johor', _('Johor')
    KEDAH = 'Kedah', _('Kedah')
    KELANTAN = 'Kelantan', _('Kelantan')
    MELAKA = 'Melaka', _('Melaka')
    NEGERI_SEMBILAN = 'Negeri Sembilan', _('Negeri Sembilan')
    PAHANG = 'Pahang', _('Pahang')
    PERAK = 'Perak', _('Perak')
    PERLIS = 'Perlis', _('Perlis')
    PENANG = 'Penang', _('Penang')
    SABAH = 'Sabah', _('Sabah')
    SARAWAK = 'Sarawak', _('Sarawak')
    SELANGOR = 'Selangor', _('Selangor')
    TERENGGANU = 'Terengganu', _('Terengganu')
    KUALA_LUMPUR = 'Kuala Lumpur', _('Kuala Lumpur')
    PUTRAJAYA = 'Putrajaya', _('Putrajaya')
    LABUAN = 'Labuan', _('Labuan')


class Coordinator(BaseUser):
    work_id = models.CharField(max_length = 255, blank=False)
    assigned_area = models.CharField(choices = STATES.choices)

    def save(self, *args, **kwargs):
        self.role = self.USER_ROLE.COORDINATOR
        super().save(*args, **kwargs)


#update photo url after adding to storage
class Report(models.Model):
    class REPORT_STATUS(models.TextChoices):
        PENDING = 'pe', _('Pending')
        APPROVED = 'ap', _('Approved')
        REJECTED = 'rj', _('Rejected')

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
    report_status = models.CharField(choices = REPORT_STATUS.choices, default=REPORT_STATUS.PENDING, max_length=2)
    state = models.CharField(choices = STATES.choices)

    category = models.CharField(choices = CATEGORY.choices, default=CATEGORY.OTHER, max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    photo_url = models.TextField(null=True, blank=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_reports') #related name for related obj back to current

    def __str__(self):
        return str(self.title)
    
    @property
    def days_since_creation(self):
        diff = timezone.now() - self.created_at
        return diff.days

#update validated_by&at
class ActiveReport(models.Model):
    class CASE_STATUS(models.TextChoices):
        IN_PROGRESS = 'ip', _('In Progress')
        COMPLETED = 'cp', _('Completed')
        CLOSED = 'cl', _('Closed')
        
    report = models.ForeignKey(Report, primary_key=True, on_delete=models.CASCADE, null=False, blank=False, related_name='active_report')
    case_progress = models.TextField(default='IN_PROGRESS', null=True, blank=True, max_length=500)
    case_status = models.CharField(choices = CASE_STATUS.choices, default=CASE_STATUS.IN_PROGRESS, max_length=2)
    
    validated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='approved_reports', limit_choices_to={ 'role': BaseUser.USER_ROLE.ADMIN })
    validated_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    manage_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='managed_reports', limit_choices_to={ 'role': BaseUser.USER_ROLE.COORDINATOR })


class CoordinatorRegistration(models.Model):
    class REGSTATUS(models.TextChoices):
        PENDING = 'pe', _('Pending')
        APPROVED = 'ap', _('Approved')
        REJECTED = 'rj', _('Rejected')

    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    
    ic_num = models.CharField(max_length=12, null=True, blank=True, unique=True)
    full_name = models.CharField(blank=False)
    phone_num = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(blank=False)
    status = models.CharField(choices = REGSTATUS.choices, default=REGSTATUS.PENDING)
    work_id = models.CharField(max_length = 255, blank=False)
    assigned_area = models.CharField(choices = STATES.choices)
    decision_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='managed_reports', limit_choices_to={ 'role': BaseUser.USER_ROLE.ADMIN })
    password = models.CharField(_("password"), max_length=128) #taken from AbstractBaseUser 

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    description = description = models.TextField(null=True,default=None, blank=True, max_length=200)
    sent_at = models.DateTimeField()
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='notification')
    
    def get_report_title(self):
        return self.report_id.title
    
    def __str__(self):
        return str(self.id)
