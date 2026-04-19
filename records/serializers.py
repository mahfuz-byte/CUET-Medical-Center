from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Inventory, Medicine, MedicalRecord

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'


User = get_user_model()


class MedicalRecordSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(write_only=True, required=False)
    student_student_id = serializers.CharField(source='student.student_id', read_only=True)
    student_email = serializers.EmailField(source='student.email', read_only=True)
    doctor_name = serializers.CharField(source='doctor.first_name', read_only=True)

    class Meta:
        model = MedicalRecord
        fields = [
            'id',
            'student',
            'student_id',
            'student_student_id',
            'student_email',
            'doctor',
            'doctor_name',
            'diagnosis',
            'prescribed_medicines',
            'advice',
            'created_at',
        ]
        read_only_fields = ['id', 'student', 'doctor', 'created_at']

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.method == 'POST':
            sid = (attrs.get('student_id') or '').strip()
            if not sid:
                raise serializers.ValidationError({'student_id': 'Student ID is required.'})

            # Accept either plain numeric ID (2204092) or full student email.
            sid_value = sid
            sid_lower = sid.lower()
            if sid_lower.startswith('u') and sid_lower.endswith('@student.cuet.ac.bd'):
                sid_value = sid_lower[1:].split('@', 1)[0]

            try:
                student = User.objects.get(
                    Q(student_id=sid_value) | Q(email__iexact=f'u{sid_value}@student.cuet.ac.bd'),
                    role='student',
                    is_active=True,
                )
            except User.DoesNotExist:
                raise serializers.ValidationError({'student_id': 'No active student found for this Student ID.'})
            except User.MultipleObjectsReturned:
                student = User.objects.filter(
                    Q(student_id=sid_value) | Q(email__iexact=f'u{sid_value}@student.cuet.ac.bd'),
                    role='student',
                    is_active=True,
                ).order_by('-student_id').first()

            attrs['student_obj'] = student
        return attrs

    def create(self, validated_data):
        student = validated_data.pop('student_obj')
        validated_data.pop('student_id', None)
        request = self.context.get('request')
        doctor = request.user if request else None
        return MedicalRecord.objects.create(student=student, doctor=doctor, **validated_data)
