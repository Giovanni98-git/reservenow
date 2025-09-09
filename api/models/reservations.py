from django.db import models
from .users import User
from .tableSaloons import TableSaloon

class Reservation(models.Model):
    date = models.DateField()
    hour = models.TimeField()
    people_count = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("completed", "Completed"), ("canceled", "Canceled")],
        default="pending"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    table_saloon = models.ForeignKey(TableSaloon, on_delete=models.SET_NULL, null=True, related_name="reservations")

    def __str__(self):
        return f"Book by {self.user.first_name} {self.user.last_name} on {self.date} at {self.hour}"
