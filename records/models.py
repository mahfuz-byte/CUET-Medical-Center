from django.db import models

class Inventory(models.Model):
    ITEM_TYPES = [
        ('kit', 'Test Kit'),
        ('bed', 'Bed'),
    ]
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    name = models.CharField(max_length=100, unique=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.item_type})"

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)

    def __str__(self):
        return self.name
