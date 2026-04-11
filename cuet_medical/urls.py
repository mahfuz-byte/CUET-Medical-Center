from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from django.views.generic import TemplateView
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/roster/', include('roster.urls')),
    path('api/records/', include('records.urls')),
    path('api/notifications/', include('notifications.urls')),
    # Serve frontend static HTML files
    path('', serve, {'document_root': os.path.join(settings.BASE_DIR, 'frontend-temp'), 'path': 'index.html'}),
    path('<path:path>', serve, {'document_root': os.path.join(settings.BASE_DIR, 'frontend-temp')}),
]

# Serve static files in development (already handled by django.contrib.staticfiles)
if settings.DEBUG:
    urlpatterns += [
        path('assets/<path:path>', serve, {'document_root': os.path.join(settings.BASE_DIR, 'frontend-temp', 'assets')}),
    ]
