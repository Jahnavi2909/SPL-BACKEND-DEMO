from rest_framework import serializers
from .models import Venue
 
class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'
 
    
    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Capacity must be greater than 0")
        return value
 
    def validate_contact_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone must contain only digits")
        return value
   
from .models import Sponsor
 
class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'
 
    def validate_website(self, value):
        if not value.startswith("http"):
            raise serializers.ValidationError("Website must start with http/https")
        return value
 