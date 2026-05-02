from django.db import models

class CallAnalysis(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    audio_file = models.FileField(upload_to='recordings/')
    transcript = models.TextField(blank=True, null=True)
    intent = models.CharField(max_length=100, blank=True, null=True)
    intent_confidence = models.FloatField(default=0.0)
    urgency_level = models.CharField(max_length=20, blank=True, null=True) # high/medium/low
    routing_department = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Analysis {self.id} - {self.status}"
