import json
import time
from urllib import error, request
import sys

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class GroqHealthAssistantView(APIView):
    permission_classes = [AllowAny]

    def post(self, request_obj):
        question = (request_obj.data.get('question') or '').strip()
        if not question:
            return Response({'detail': 'Question is required.'}, status=status.HTTP_400_BAD_REQUEST)

        api_key = (settings.GROQ_API_KEY or '').strip()
        if not api_key:
            return Response(
                {'detail': 'GROQ_API_KEY is not configured on the server.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Debug: Print API key status
        print(f"DEBUG - API Key loaded: {api_key[:10]}...", file=sys.stderr)

        system_prompt = (
            'You are a campus health assistant for CUET Medical Center. '
            'Provide only general health information and wellness advice. '
            'Do not diagnose diseases or provide medical prescriptions. '
            'For emergencies or serious concerns, advise users to contact a doctor or emergency services immediately.'
        )

        payload = {
            'messages': [
                {
                    'role': 'system',
                    'content': system_prompt,
                },
                {
                    'role': 'user',
                    'content': question,
                }
            ],
            'model': 'mixtral-8x7b-32768',
            'temperature': 0.4,
            'max_tokens': 500,
        }

        endpoint = 'https://api.groq.com/openai/v1/chat/completions'

        print(f"DEBUG - Payload: {json.dumps(payload)[:200]}", file=sys.stderr)
        print(f"DEBUG - Endpoint: {endpoint}", file=sys.stderr)

        req = request.Request(
            endpoint,
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
            },
            method='POST',
        )

        try:
            with request.urlopen(req, timeout=20) as response:
                data = json.loads(response.read().decode('utf-8'))
                print(f"DEBUG - Response: {json.dumps(data)[:200]}", file=sys.stderr)
        except error.HTTPError as exc:
            detail = exc.read().decode('utf-8', errors='ignore') if exc.fp else str(exc)
            print(f"DEBUG - Groq API HTTP Error {exc.code}: {detail}", file=sys.stderr)
            detail_lower = detail.lower()
            if exc.code == 429 or 'quota' in detail_lower or 'rate' in detail_lower:
                return Response({'detail': 'Rate limit reached. Please try again later.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            return Response({'detail': f'Groq API error: {detail[:500]}'}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as exc:
            print(f"DEBUG - Groq API Connection Error: {str(exc)}", file=sys.stderr)
            return Response({'detail': f'Failed to connect to Groq API: {str(exc)}'}, status=status.HTTP_502_BAD_GATEWAY)

        # Extract answer from Groq API response
        choices = data.get('choices') or []
        if not choices:
            answer = 'Sorry, I could not generate an answer right now. Please try again.'
        else:
            message = choices[0].get('message') or {}
            answer = message.get('content', '').strip()
            if not answer:
                answer = 'Sorry, I could not generate an answer right now. Please try again.'

        return Response({'answer': answer}, status=status.HTTP_200_OK)
