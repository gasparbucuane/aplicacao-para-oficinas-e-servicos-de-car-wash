# project/urls.py

from django.urls import path, include
from core.views import home  # Importe a view

urlpatterns = [

    path('', home, name='home'),  # Rota para a home page

]
