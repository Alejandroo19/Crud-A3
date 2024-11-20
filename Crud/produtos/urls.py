from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
    path('estoque_baixo/', views.ver_estoque_baixo, name='ver_estoque_baixo'),
    path('procurar/', views.procurar_produto, name='procurar_produto'),
    path('gerenciar_categorias/', views.gerenciar_categorias,name='gerenciar_categorias'),
    path('historico_movimentacoes/', views.historico_movimentacoes, name='historico_movimentacoes'),
    path('editar_categoria/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('deletar_categoria/<int:categoria_id>/', views.deletar_categoria, name='deletar_categoria'),
    path('ativar_desativar_categoria/<int:categoria_id>/', views.ativar_desativar_categoria, name='ativar_desativar_categoria'),
    path('editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),
    path('historico_movimentacoes/', views.historico_movimentacoes, name='historico_movimentacoes'),
    path('movimentar_produto/<int:produto_id>/', views.movimentar_produto, name='movimentar_produto'),
    path('ativar_desativar_produto/<int:produto_id>/', views.ativar_desativar_produto, name='ativar_desativar_produto'),
]

path('editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),
