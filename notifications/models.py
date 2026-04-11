from django.db import models
from django.conf import settings

class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    target = models.CharField(max_length=50, default='all', choices=[
        ('all', 'All Users'),
        ('students', 'Students Only'),
        ('doctors', 'Doctors Only'),
    ])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_notifications')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
