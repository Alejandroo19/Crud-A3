from django.contrib import admin
from .models import Produto
from .models import Categoria

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'categoria', 'preco', 'quantidade')

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria)