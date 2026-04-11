import json
import time
from urllib import error, request

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class GeminiHealthAssistantView(APIView):
    permission_classes = [AllowAny]

    def post(self, request_obj):
        question = (request_obj.data.get('question') or '').strip()
        if not question:
            return Response({'detail': 'Question is required.'}, status=status.HTTP_400_BAD_REQUEST)

        api_key = (settings.GEMINI_API_KEY or '').strip()
        if not api_key or api_key == 'YOUR_REAL_GEMINI_API_KEY':
            return Response(
                {'detail': 'GEMINI_API_KEY is not configured on the server.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        prompt = (
            'You are a campus health assistant. Provide only general health information. '
            'Do not diagnose disease. For emergencies, tell users to contact a doctor or emergency services.'
        )

        payload = {
            'contents': [
                {
                    'parts': [
                        {'text': prompt},
                        {'text': f'User question: {question}'},
                    ]
                }
            ],
            'generationConfig': {
                'temperature': 0.4,
                'maxOutputTokens': 500,
            },
        }

        # Free-tier model only.
        model_name = 'gemini-1.5-flash'
        endpoint = (
            'https://generativelanguage.googleapis.com/v1beta/models/'
            f'{model_name}:generateContent?key={api_key}'
        )

        req = request.Request(
            endpoint,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST',
        )

        # Small delay to reduce accidental burst requests on free tier.
        time.sleep(2)

        try:
            with request.urlopen(req, timeout=20) as response:
                data = json.loads(response.read().decode('utf-8'))
        except error.HTTPError as exc:
            detail = exc.read().decode('utf-8', errors='ignore') if exc.fp else str(exc)
            detail_lower = detail.lower()
            if exc.code == 429 or 'quota' in detail_lower or 'rate' in detail_lower:
                return Response({'detail': 'Free quota reached. Try again later.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            return Response({'detail': f'Gemini API error: {detail[:500]}'}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as exc:
            return Response({'detail': f'Failed to connect to Gemini API: {exc}'}, status=status.HTTP_502_BAD_GATEWAY)

        candidates = data.get('candidates') or []
        content = (candidates[0].get('content') if candidates else {}) or {}
        parts = content.get('parts') or []
        answer = (parts[0].get('text') if parts and isinstance(parts[0], dict) else '') or ''
        answer = answer.strip()

        if not answer:
            answer = 'Sorry, I could not generate an answer right now. Please try again.'

        return Response({'answer': answer}, status=status.HTTP_200_OK)
