from django.contrib import admin
from django.urls import path, include
from produtos import views as produtos_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('produtos.urls')),  # Inclui as URLs do app produtos
    path('gerenciar_categorias/', produtos_views.gerenciar_categorias, name='gerenciar_categorias'),
    path('historico_movimentacao/', produtos_views.historico_movimentacao, name='historico_movimentacao'),
]
