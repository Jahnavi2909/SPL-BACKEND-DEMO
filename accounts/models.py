from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('FRANCHISE', 'Franchise'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class Franchise(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="franchise")
    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    address = models.TextField()
    logo = models.ImageField(upload_to='franchise_logos/',null=True,blank=True)
    website = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name