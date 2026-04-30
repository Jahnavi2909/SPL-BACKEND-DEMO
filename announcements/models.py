from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
 
 
class Announcements(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    tournament_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
 
    def clean(self):
        if self.expires_at <= timezone.now():
            raise ValidationError("Expiry date must be in future")
 
    def __str__(self):
        return self.title
 
 
class News(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
 
    def clean(self):
        if self.expires_at <= timezone.now():
            raise ValidationError("Expiry date must be in future")
 
    def __str__(self):
        return self.title
 