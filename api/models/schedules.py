from django.db import models

class Schedule(models.Model):
    day = models.CharField(max_length=20)
    message = models.CharField(max_length=200, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def is_open(self, date_time):
        
        return self.opening_time <= date_time.time() <= self.closing_time

    def __str__(self):
        return f"schedule for {self.day}"