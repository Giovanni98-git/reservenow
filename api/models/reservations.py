from django.db import models 
from .users import User
from .tableSalons import TableSalon

class Reservation(models.Model):
    date = models.DateField()
    heure = models.TimeField()
    nb_personnes = models.PositiveIntegerField()
    statut = models.CharField(
        max_length=20,
        choices=[('confirm', 'Confirmée'), ('completed', 'Complétée'), ('canceled', 'Annulée')],
        default='confirm'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    table_salon = models.ForeignKey(TableSalon, on_delete=models.SET_NULL, null=True, related_name='reservations')

    def __str__(self):
        return f"Réservation par {self.user} le {self.date} à {self.heure}"