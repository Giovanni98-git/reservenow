from django.db import models
from django.utils import timezone
from .users import User
from .reservations import Reservation

class Notification(models.Model):
    type = models.CharField(
        max_length=10,
        choices=[("email", "Email"), ("sms", "SMS")]
    )
    message = models.TextField()
    sending_date = models.DateTimeField(default=timezone.now)
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, null=True, blank=True, related_name="notifications"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")

    def send(self):
        return True

    def __str__(self):
        return f"Notification ({self.type})"
