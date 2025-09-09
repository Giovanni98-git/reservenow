from django.db import models
from .users import User

class Report(models.Model):
    period = models.CharField(max_length=50)
    occupancy_rate = models.FloatField()
    nb_annulation = models.IntegerField(default=0)
    pics_activity = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reports")

    def generate_csv(self):
        return "CSV data"

    def generate_json(self):
        return {"data": "JSON"}

    def __str__(self):
        return f"Report for {self.period}"
