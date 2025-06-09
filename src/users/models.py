from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import TextChoices

from stocks.models import Warehouse

# Get the currently active user model
user = get_user_model()


# User profile model
class UserProfile(models.Model):
    # Different user profiles in the company
    class Profiles(TextChoices):
        ADMIN = "ADM", "Admin"
        MANAGER = "MAN", "Manager"
        OPERATOR = "OPE", "Operator"
        USER = "USR", "User"

    # Link to the User model
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name="user")
    # Link to the Warehouse model: where the user can access
    warehouses = models.ManyToManyField(Warehouse, related_name="warehouses")
    # User's profile, a simple user by default
    profile = models.CharField(max_length=10, default=Profiles.USER, choices=Profiles, verbose_name="user profile")

    def __str__(self):
        return f"{self.user} ({self.profile})"
