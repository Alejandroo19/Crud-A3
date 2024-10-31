from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
    path('estoque_baixo/', views.ver_estoque_baixo, name='ver_estoque_baixo'),
    path('procurar/', views.procurar_produto, name='procurar_produto'),
]

path('editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),
