from rest_framework import serializers
from . import models


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contact
        fields = '__all__'

    def validate_email(self, attrs):
        if 'gmail' in attrs:
            raise serializers.ValidationError("Google Domain is not supported")
        return attrs
