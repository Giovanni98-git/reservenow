from django.db import models

class Horaire(models.Model):
    jour = models.CharField(max_length=20)
    message = models.CharField(max_length=200, blank=True)
    heure_ouverture = models.TimeField()
    heure_fermeture = models.TimeField()

    def est_ouvert(self, date_heure):
        
        return self.heure_ouverture <= date_heure.time() <= self.heure_fermeture

    def __str__(self):
        return f"Horaire pour {self.jour}"