from django.contrib import admin
from .models import Produto

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'categoria', 'preco', 'quantidade')

admin.site.register(Produto, ProdutoAdmin)