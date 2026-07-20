from rest_framework import serializers

from core.models import FarmerProfile, Notice, PorterProfile

# admin/cooperative farmer account
class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model= FarmerProfile 
        fields='__all__'

# Porter
class PorterSerializer(serializers.ModelSerializer):
    class Meta:
        model= PorterProfile 
        fields='__all__'

# Notices 
class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notice
        fields='__all__'
        read_only_fields=['created_by']