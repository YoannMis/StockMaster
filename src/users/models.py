from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import TextChoices

from stocks.models import Warehouse

# Get the currently active user model
user = get_user_model()


# User profile model
class UserProfile(models.Model):
    # Different user profiles in the company
    class Profiles(TextChoices): # Tu pourrais aussi utiliser les permissions de Django, mais ton choix est valable :)
        ADMIN = "ADM", "Admin"
        MANAGER = "MAN", "Manager"
        OPERATOR = "OPE", "Operator"
        USER = "USR", "User"

    # Link to the User model
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name="user")
    # Link to the Warehouse model: where the user can access
    warehouses = models.ManyToManyField(Warehouse, related_name="warehouses") # Un utilisateur peut avoir accès à plusieurs entrepôts du coup ? si c'est ça ok
    # User's profile, a simple user by default
    profile = models.CharField(max_length=10, default=Profiles.USER, choices=Profiles, verbose_name="user profile")

    def __str__(self):
        return f"{self.user} ({self.profile})"


"""
Tu pourrais aussi faire un modèle de type StoreUser qui contiendrait un lien vers le modèle 
User et un lien vers le modèle Store, et un champ pour le rôle de l'utilisateur dans le magasin. Par exemple :
class AccountStore(models.Model): ## Ici je ferais du coup AccountStore
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.ForeignKey("account.Role", on_delete=models.CASCADE) # ou ManyToMany s'il y a plusieurs roles possibles
    date_created = models.DateTimeField(auto_now=True)
"""
