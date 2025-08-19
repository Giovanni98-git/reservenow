from django.db import models

class TableSalon(models.Model):
    capacite = models.PositiveIntegerField()
    type = models.CharField(
        max_length=20,
        choices=[('table', 'Table'), ('salon', 'Salon')]
    )
    statut = models.CharField(
        max_length=20,
        choices=[('disponible', 'Disponible'), ('indisponible', 'Indisponible')],
        default='disponible'
    )

    def update_disponibilite(self, disponible: bool):
        self.statut = 'disponible' if disponible else 'indisponible'
        self.save()

    def __str__(self):
        return f"{self.type} (Capacité: {self.capacite})"
