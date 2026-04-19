from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from django.views.generic import TemplateView
from cuet_medical.views import GroqHealthAssistantView
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/roster/', include('roster.urls')),
    path('api/records/', include('records.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/assistant/ask/', GroqHealthAssistantView.as_view(), name='groq-assistant'),
    # Serve static/media files in development BEFORE the catch-all patterns
    path('assets/<path:path>', serve, {'document_root': os.path.join(settings.BASE_DIR, 'frontend-temp', 'assets')}),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    # Serve frontend static HTML files (catch-all at the end)
    path('', serve, {'document_root': os.path.join(settings.BASE_DIR, 'frontend-temp'), 'path': 'index.html'}),
    path('<path:path>', serve, {'document_root': os.path.join(settings.BASE_DIR, 'frontend-temp')}),
]
