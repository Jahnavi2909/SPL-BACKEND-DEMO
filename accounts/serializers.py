from rest_framework import serializers
from .models import Franchise
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer




from rest_framework import serializers
from .models import Franchise

class FranchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise
        fields = '__all__'

    def update(self, instance, validated_data):
        user = self.context['request'].user

        # Fields allowed for franchise user
        allowed_fields = [
            'company_name',
            'owner_name',
            'contact_email',
            'contact_phone',
            'address',
            'logo',
            'website'
        ]

        # ✅ If user is franchise → restrict fields
        if user.role == 'FRANCHISE':
            for field in list(validated_data.keys()):
                if field not in allowed_fields:
                    validated_data.pop(field)

        # Admin can update everything
        return super().update(instance, validated_data)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add extra fields
        data['username'] = self.user.username
        data['role'] = self.user.role

        # Add franchise_id if exists
        if hasattr(self.user, 'franchise'):
            data['franchise_id'] = self.user.franchise.id
        else:
            data['franchise_id'] = None

        return data