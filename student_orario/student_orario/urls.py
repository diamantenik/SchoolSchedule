from django.contrib import admin
from django.urls import path, include
from scuola import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scuola.urls'))
]