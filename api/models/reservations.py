from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import time
from .users import User
from .tableSaloons import TableSaloon


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]

    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    people_count = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations"
    )
    table_saloon = models.ForeignKey(
        TableSaloon,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reservations"
    )

    class Meta:
        indexes = [
            models.Index(fields=["table_saloon", "date", "start", "end"]),
        ]
        ordering = ["date", "start"]
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"

    def clean(self):
        """Validation logique métier universelle."""
        # Vérifie la cohérence horaire
        if self.end <= self.start:
            raise ValidationError("L'heure de fin doit être supérieure à l'heure de début.")

        # Vérifie la capacité du salon/table
        if self.table_saloon and self.people_count > self.table_saloon.capacity:
            raise ValidationError(
                f"Le nombre de personnes ({self.people_count}) dépasse la capacité "
                f"de la table/salon ({self.table_saloon.capacity})."
            )

        # Vérifie le chevauchement des réservations actives
        if self.table_saloon and self.date:
            overlapping = Reservation.objects.filter(
                table_saloon=self.table_saloon,
                date=self.date,
                status__in=["pending", "completed"],
                start__lt=self.end,
                end__gt=self.start
            ).exclude(pk=self.pk)

            if overlapping.exists():
                raise ValidationError(
                    f"La table/salon {self.table_saloon} est déjà réservée sur cet intervalle."
                )

    def save(self, *args, **kwargs):
        """S’assure que la validation est toujours effectuée avant la sauvegarde."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        user_name = f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
        return f"Réservation par {user_name} le {self.date} de {self.start} à {self.end}"
