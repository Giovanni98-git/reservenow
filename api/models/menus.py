from django.db import models
from .users import User

class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="menus")

    def __str__(self):
        return self.name
