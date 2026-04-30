from django.contrib import admin
from .models import Venue
 
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['ground_name', 'city', 'capacity', 'contact_person']
    search_fields = ['ground_name', 'city']
 
from .models import Sponsor
 
@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['sponsor_name', 'website', 'contact_email']
    search_fields = ['sponsor_name']