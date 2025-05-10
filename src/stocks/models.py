from django.db import models


class Warehouse(models.Model):
    class Type(models.TextChoices):
        STORE = "Store", "Magasin"
        KANBAN = "Kanban"

    name = models.CharField(max_length=50, verbose_name="Name")
    location = models.CharField(max_length=50, verbose_name="location")

    def __str__(self):
        return self.name
