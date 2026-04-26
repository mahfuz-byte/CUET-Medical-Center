#!/usr/bin/env python
"""Test script to verify alerts API works correctly"""
import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cuet_medical.settings')
django.setup()

from accounts.models import User
from notifications.models import Notification
from rest_framework_simplejwt.tokens import RefreshToken

def test_alerts_api():
    # Get a doctor user
    doctor = User.objects.filter(role='doctor').first()
    if not doctor:
        print("❌ No doctor users found")
        return
    
    print(f"✅ Found doctor: {doctor.first_name} {doctor.last_name}")
    
    # Generate token for the doctor
    refresh = RefreshToken.for_user(doctor)
    access_token = str(refresh.access_token)
    print(f"✅ Generated access token: {access_token[:20]}...")
    
    # Test 1: Check if alerts endpoint is accessible
    from django.test import Client
    from rest_framework.test import APIClient
    
    client = APIClient()
    
    # Test GET (should work without auth)
    print("\n📝 Testing GET /api/notifications/")
    response = client.get('/api/notifications/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        alerts = data.get('results', data) if isinstance(data, dict) else data
        print(f"   Alerts found: {len(alerts) if isinstance(alerts, list) else 'N/A'}")
    else:
        print(f"   Error: {response.content}")
    
    # Test POST (should require auth and doctor role)
    print("\n📝 Testing POST /api/notifications/ with auth")
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    alert_data = {
        'title': 'Test Alert',
        'message': 'This is a test alert',
        'target': 'all'
    }
    
    response = client.post('/api/notifications/', alert_data, format='json')
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    if response.status_code in [200, 201]:
        print("✅ Alert created successfully!")
        # Verify it's in database
        alert_count = Notification.objects.count()
        print(f"   Total alerts in DB: {alert_count}")
    else:
        print(f"❌ Failed to create alert")
        print(f"   Reason: {response.json()}")

if __name__ == '__main__':
    print("🧪 Testing Alerts API\n")
    test_alerts_api()
