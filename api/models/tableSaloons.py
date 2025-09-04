from django.db import models

class TableSaloon(models.Model):
    capacity = models.PositiveIntegerField()
    name = models.CharField(max_length=255, null=False)
    type = models.CharField(
        max_length=20,
        choices=[('table', 'Table'), ('saloon', 'Saloon')]
    )
    status = models.CharField(
        max_length=20,
        choices=[('available', 'Available'), ('unavailable', 'Unavailable')],
        default='available'
    )

    def update_availability(self, availability: bool):
        self.status = 'available' if availability else 'unavailable'
        self.save()

    def __str__(self):
        return f"{self.type} (Capacity: {self.capacity}, status: {self.status})"
