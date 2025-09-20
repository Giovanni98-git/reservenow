from django.db import models
from .users import User

class MenuManager(models.Manager):
    def create_from_json(self, data, user):
        """Crée une entrée de menu à partir des données JSON et d'un utilisateur."""
        return self.create(
            name=data['dsc'],
            description=data['name'], 
            price=data['price'],
            rate=data['rate'],
            country=data['country'],
            img=data['img'],
            user=user
        )

class Menu(models.Model):
    name = models.CharField(max_length=200, unique=True) 
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=40.0)
    rate = models.PositiveIntegerField(default=0)
    country = models.CharField(max_length=100, blank=True)
    img = models.URLField(max_length=500, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="menus")
    
    objects = MenuManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"