from django.db import models
from .users import User

class Rapport(models.Model):
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
        return f"Rapport pour {self.periode}"