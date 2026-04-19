from django.db import models
from django.conf import settings

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


class MedicalRecord(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='medical_records',
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctor_created_records',
    )
    diagnosis = models.CharField(max_length=255)
    prescribed_medicines = models.TextField()
    advice = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.email} - {self.diagnosis}"
