from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Doctor, Ambulance
from .serializers import DoctorSerializer, AmbulanceSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]

class AmbulanceViewSet(viewsets.ModelViewSet):
    queryset = Ambulance.objects.all()
    serializer_class = AmbulanceSerializer
    permission_classes = [AllowAny]

