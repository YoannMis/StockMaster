from django.db import models
from django.contrib.auth.models import User
from stocks.models import Warehouse


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    warehouses = models.ManyToManyField(Warehouse, related_name='user_profiles')

    # def __str__(self):
    #     return self.user.name
