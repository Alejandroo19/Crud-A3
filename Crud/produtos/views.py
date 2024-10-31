from django.shortcuts import render, redirect
from .models import Produto, Categoria
from .forms import ProdutoForm

# Listar produtos
def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos/lista_produtos.html', {'produtos': produtos})

# Cadastrar produto
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/cadastrar_produto.html', {'form': form})

# Ver produtos com estoque baixo
def ver_estoque_baixo(request):
    produtos = Produto.objects.filter(quantidade__lte=models.F('quantidade_minima'))
    return render(request, 'produtos/lista_produtos.html', {'produtos': produtos})

# Procurar produto
def procurar_produto(request):
    query = request.GET.get('query', '')
    produtos = Produto.objects.filter(nome__icontains=query)
    return render(request, 'produtos/lista_produtos.html', {'produtos': produtos})
from django.shortcuts import get_object_or_404

# editar produto
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    
    return render(request, 'produtos/editar_produto.html', {'form': form, 'produto': produto})
