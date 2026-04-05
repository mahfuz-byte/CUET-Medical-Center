from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    dept = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    hours = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Ambulance(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('On Duty', 'On Duty'),
        ('Maintenance', 'Maintenance'),
    ]
    ambulance_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    contact = models.CharField(max_length=50)

    def __str__(self):
        return self.ambulance_id
