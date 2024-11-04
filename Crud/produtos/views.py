from django.shortcuts import render, redirect
from .models import Produto, Categoria
from .forms import ProdutoForm
from .models import Categoria, Movimentacao
from django.contrib import messages 

# Listar produtos
def lista_produtos(request):
    produtos = Produto.objects.all()
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('lista_produtos')
        else:
            messages.error(request, 'Erro ao cadastrar produto. Verifique os dados informados.')
    else:
        form = ProdutoForm()

    return render(request, 'produtos/lista_produtos.html', {'produtos': produtos, 'form': form})
# Cadastrar produto
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/lista_produtos.html', {'form': form})

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

def gerenciar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'produtos/gerenciar_categorias.html', {'categorias': categorias})

def historico_movimentacao(request):
    movimentacoes = Movimentacao.objects.all()
    return render(request, 'produtos/historico_movimentacao.html', {'movimentacoes': movimentacoes})