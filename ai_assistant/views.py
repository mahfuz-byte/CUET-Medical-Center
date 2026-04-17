from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
import google.generativeai as genai
from .serializers import ChatMessageSerializer, ChatHistorySerializer
from .models import ChatHistory
from roster.models import Doctor, Ambulance
from records.models import Medicine
import os

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)


def get_medical_context():
    """Fetch medical center data from database to provide context"""
    try:
        # Get doctor roster
        doctors = Doctor.objects.all()
        doctor_list = []
        for doc in doctors:
            doctor_list.append(f"- Dr. {doc.name}, {doc.title}, Department: {doc.dept}, Hours: {doc.hours}")
        
        # Get ambulance status
        ambulances = Ambulance.objects.all()
        ambulance_list = []
        for amb in ambulances:
            ambulance_list.append(f"- {amb.ambulance_id}: {amb.status} (Contact: {amb.contact})")
        
        # Get medicines
        medicines = Medicine.objects.all()
        medicine_list = [med.name for med in medicines[:10]]  # Limit to 10
        
        context = f"""
CUET MEDICAL CENTER INFORMATION:
================================

AVAILABLE DOCTORS:
{chr(10).join(doctor_list) if doctor_list else 'No doctors available'}

AMBULANCE SERVICES:
{chr(10).join(ambulance_list) if ambulance_list else 'No ambulances available'}

AVAILABLE MEDICINES:
{', '.join(medicine_list) if medicine_list else 'No medicines listed'}

SERVICES PROVIDED:
- Medical Consultation
- Emergency Ambulance Services
- Blood Bank Services
- Medical Records Management
- Prescription Management
- Bed Availability Checking
- Test Kit Availability
"""
        return context
    except Exception as e:
        return f"Error fetching context: {str(e)}"


def build_system_prompt():
    """Build system prompt with medical center context"""
    medical_context = get_medical_context()
    
    system_prompt = f"""You are a helpful AI Health Assistant for CUET Medical Center. 
You provide information about:
1. Doctor availability and expertise
2. Ambulance services and emergency support
3. Medicines and treatment advice
4. Viral disease information (based on general knowledge)
5. Diet plans and nutrition advice
6. Stress relief and mental health tips
7. First aid techniques
8. General health and wellness guidance

{medical_context}

IMPORTANT GUIDELINES:
- Always be helpful and professional
- For serious medical conditions, recommend visiting a doctor
- When mentioning doctors from our center, provide their details
- For ambulance emergencies, mention the contact and available ambulances
- Provide accurate health information based on your training data
- If asked about something outside your expertise, politely redirect to our medical center staff

Be concise but informative in your responses."""
    
    return system_prompt


@api_view(['POST'])
@permission_classes([AllowAny])  # Unregistered users can use this
def chat_with_ai(request):
    """
    Chat endpoint that integrates with Gemini API and provides context
    from the medical center database
    """
    serializer = ChatMessageSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user_message = serializer.validated_data['message']
    
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=build_system_prompt()
        )
        
        # Generate response
        response = model.generate_content(user_message)
        ai_response = response.text
        
        # Save chat history if user is authenticated
        if request.user.is_authenticated:
            ChatHistory.objects.create(
                user=request.user,
                user_message=user_message,
                ai_response=ai_response
            )
        
        return Response({
            'user_message': user_message,
            'ai_response': ai_response
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        error_message = str(e)
        
        # Provide user-friendly error messages
        if 'quota' in error_message.lower() or 'resource_exhausted' in error_message.lower():
            return Response({
                'error': 'API quota exhausted. Please try again later or contact support.'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        elif 'not found' in error_message.lower():
            return Response({
                'error': 'Model not available. Please contact support.'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'error': f'Failed to generate response: {error_message[:100]}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChatHistoryView(generics.ListAPIView):
    """Get chat history for authenticated users"""
    serializer_class = ChatHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatHistory.objects.filter(user=self.request.user)
