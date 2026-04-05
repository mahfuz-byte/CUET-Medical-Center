from rest_framework import serializers
from .models import BloodDonor, BloodRequest
from accounts.serializers import UserSerializer


class BloodDonorSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = BloodDonor
        fields = ['id', 'user', 'user_detail', 'blood_group', 'phone', 'is_available', 'last_donation_date']
        read_only_fields = ['id', 'user']


class BloodDonorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodDonor
        fields = ['blood_group', 'phone', 'is_available', 'last_donation_date']


class BloodRequestSerializer(serializers.ModelSerializer):
    requested_by_detail = UserSerializer(source='requested_by', read_only=True)
    
    class Meta:
        model = BloodRequest
        fields = ['id', 'requested_by', 'requested_by_detail', 'blood_group', 'units_needed', 'urgency', 'status', 'message', 'created_at']
        read_only_fields = ['id', 'requested_by', 'created_at']
