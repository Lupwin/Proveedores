from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('aplicacion.urls')),  # Incluye las URL de la aplicación "aplicacion"
]
