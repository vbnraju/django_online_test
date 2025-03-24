from django.db import models


class Appointment(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time_slot = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.date} {self.time_slot}"