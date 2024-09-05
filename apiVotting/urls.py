from django.contrib import admin
from django.urls import path, include  # Importe a função `include`

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # Inclua as URLs do seu aplicativo `myapp`
]
