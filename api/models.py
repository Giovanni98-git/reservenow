import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(
        max_length=10,
        choices=[('client', 'Client'), ('admin', 'Admin')],
        default='client'
    )
    # Les champs first_name, last_name, email, password sont hérités d'AbstractUser.
    

    def __str__(self):
        return self.username

class TableSalon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
        return f"{self.type} {self.id} (Capacité: {self.capacite})"

class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
        return f"Réservation {self.id} par {self.user} le {self.date} à {self.heure}"

class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='menus')

    def __str__(self):
        return self.nom

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(
        max_length=10,
        choices=[('email', 'Email'), ('sms', 'SMS')]
    )
    message = models.TextField()
    date_envoi = models.DateTimeField(default=timezone.now)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    def envoyer(self):
        # Logique d'envoi (
        return True 

    def __str__(self):
        return f"Notification {self.id} ({self.type})"

class Rapport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    periode = models.CharField(max_length=50)
    taux_occupation = models.FloatField()
    nb_annulation = models.IntegerField(default=0)
    pics_activite = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='rapports') 

    def generer_csv(self):
        # Logique pour générer CSV (utilise csv module)
        return "CSV data" 

    def generer_json(self):
        # Logique pour JSON
        return {"data": "JSON"} 

    def __str__(self):
        return f"Rapport {self.id} pour {self.periode}"

class Horaire(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jour = models.CharField(max_length=20)
    message = models.CharField(max_length=200, blank=True)
    heure_ouverture = models.TimeField()
    heure_fermeture = models.TimeField()

    def est_ouvert(self, date_heure):
        
        return self.heure_ouverture <= date_heure.time() <= self.heure_fermeture

    def __str__(self):
        return f"Horaire pour {self.jour}"