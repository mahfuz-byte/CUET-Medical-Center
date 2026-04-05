from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/roster/', include('roster.urls')),
    path('api/records/', include('records.urls')),
]
