from django.db import models
from django.core.exceptions import ValidationError
from datetime import time  # Import ajouté pour les valeurs par défaut
from .users import User
from .tableSaloons import TableSaloon

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import time
from .users import User
from .tableSaloons import TableSaloon

class Reservation(models.Model):
    date = models.DateField()
    start = models.TimeField()  # Valeur par défaut
    end = models.TimeField()   # Valeur par défaut
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
        # Vérifie que end > start
        if self.end <= self.start:
            raise ValidationError("L'heure de fin doit être supérieure à l'heure de début.")

        # Vérifie que people_count ne dépasse pas la capacité de la table/salon
        if self.table_saloon and self.people_count > self.table_saloon.capacity:
            raise ValidationError(
                f"Le nombre de personnes ({self.people_count}) dépasse la capacité "
                f"de la table/salon ({self.table_saloon.capacity})."
            )

        # Vérifie qu'il n'y a pas de chevauchement de réservation
        if self.table_saloon and self.date:
            overlapping = Reservation.objects.filter(
                table_saloon=self.table_saloon,
                date=self.date,
                status__in=["pending", "completed"],  # Ignorer les réservations annulées
                start__lt=self.end,
                end__gt=self.start
            ).exclude(pk=self.pk)  # Exclure la réservation actuelle si mise à jour

            if overlapping.exists():
                raise ValidationError(
                    f"La table/salon {self.table_saloon} est déjà réservée sur cet intervalle."
                )

    def __str__(self):
        # Utiliser username comme fallback si first_name/last_name sont vides
        user_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return f"Réservation par {user_name} le {self.date} de {self.start} à {self.end}"