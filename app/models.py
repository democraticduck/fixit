"""
Definition of models.
"""

from django.db import models

from django.contrib.auth.models import User, AbstractUser

#sharing entity

class Item(models.Model):
    item_id = models.CharField(primary_key=True, max_length=10)
    item_name = models.TextField()
    item_description = models.TextField(null=True,default=None, blank=True)
    def __str__(self):
        return str(self.item_id)

class User(AbstractUser):
    ic_num = models.CharField(max_length=12, null=True, blank=True, unique=True)
    phone_num = models.CharField(max_length=15, null=True, blank=True)
    pass