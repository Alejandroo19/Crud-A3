# entradas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('movimentar/', views.movimentar_produto, name='movimentar_produto'),
]
