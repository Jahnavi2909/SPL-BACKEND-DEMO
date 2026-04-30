from django.db import models
 
class Venue(models.Model):
    ground_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    capacity = models.IntegerField()
    contact_person = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20)
 
    def __str__(self):
        return self.ground_name
 
class Sponsor(models.Model):
    sponsor_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='sponsor/')
    website = models.URLField()
    contact_email = models.EmailField()
 
    def __str__(self):
        return self.sponsor_name