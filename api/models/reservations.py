from django.db import models
from django.core.exceptions import ValidationError
from .users import User
from .tableSaloons import TableSaloon

class Reservation(models.Model):
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    people_count = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("completed", "Completed"), ("canceled", "Canceled")],
        default="pending"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    table_saloon = models.ForeignKey(TableSaloon, on_delete=models.SET_NULL, null=True, related_name="reservations")

    def clean(self):
        """Validation universelle (admin, shell, API si .full_clean() est appelé)"""
        if self.end <= self.start:
            raise ValidationError("L'heure de fin doit être supérieure à l'heure de début.")

    def __str__(self):
        return f"Réservation par {self.user.first_name} {self.user.last_name} le {self.date} de {self.start} à {self.end}"
