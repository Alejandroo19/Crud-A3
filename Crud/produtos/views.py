# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Categoria, Movimentacao
from .forms import ProdutoForm
from django.contrib import messages 
from django.db import models 

def lista_produtos(request):
    produtos = Produto.objects.all()
    categorias_ativas = Categoria.objects.filter(ativo=True)

    # Debug - Verificar categorias ativas
    print("Categorias ativas (na view):", categorias_ativas)

    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        # Atualizar o queryset do campo categoria para apenas categorias ativas
        form.fields['categoria'].queryset = categorias_ativas
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('lista_produtos')
        else:
            messages.error(request, 'Erro ao cadastrar produto. Verifique os dados informados.')
    else:
        form = ProdutoForm()
        # Atualizar o queryset do campo categoria para apenas categorias ativas
        form.fields['categoria'].queryset = categorias_ativas

    # Debug - Verificar o queryset após a atualização
    print("Updated queryset for categories:", form.fields['categoria'].queryset)

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
    nome = request.GET.get('nome', '').strip()
    codigo = request.GET.get('codigo', '').strip()
    categoria_id = request.GET.get('categoria', '')
    incluir_ativos = request.GET.get('incluir_ativos', 'on') == 'on'
    incluir_inativos = request.GET.get('incluir_inativos', '') == 'on'
    incluir_estoque_baixo = request.GET.get('incluir_estoque_baixo', '') == 'on'

    # Inicia o queryset de produtos
    produtos = Produto.objects.all()

    # Filtra pelo nome, se informado
    if nome:
        produtos = produtos.filter(nome__icontains=nome)

    # Filtra pelo código, se informado
    if codigo:
        produtos = produtos.filter(codigo__icontains=codigo)

    # Filtra pela categoria, se selecionada
    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)

    # Filtrar por status (ativos ou inativos)
    if not (incluir_ativos and incluir_inativos):
        if incluir_ativos:
            produtos = produtos.filter(ativo=True)
        elif incluir_inativos:
            produtos = produtos.filter(ativo=False)

    # Filtrar por estoque baixo, se selecionado
    if incluir_estoque_baixo:
        produtos = produtos.filter(quantidade__lte=models.F('quantidade_minima'))

    return render(request, 'produtos/lista_produtos.html', {'produtos': produtos})

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

def historico_movimentacoes(request):
    movimentacoes = Movimentacao.objects.all()  # Corrigir para garantir que `movimentacoes` esteja sempre definida.
    return render(request, 'produtos/historico_movimentacoes.html', {'movimentacoes': movimentacoes})

# View para gerenciar categorias (cadastrar, editar e excluir)
def gerenciar_categorias(request):
    if request.method == 'POST' and 'categoria_nome' in request.POST:
        # Cadastro de nova categoria
        nome = request.POST.get('categoria_nome')
        Categoria.objects.create(nome=nome)
        return redirect('gerenciar_categorias')
    
    categorias = Categoria.objects.all()
    return render(request, 'produtos/gerenciar_categorias.html', {'categorias': categorias})

def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        nome = request.POST.get('categoria_nome')
        categoria.nome = nome
        categoria.save()
        return redirect('gerenciar_categorias')

def deletar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('gerenciar_categorias')
    
    # View para ativar/desativar uma categoria
def ativar_desativar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.ativo = not categoria.ativo  # Alterna o status ativo/desativado
    categoria.save()
    return redirect('gerenciar_categorias')

def movimentar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        operacao = request.POST.get('operacao')
        quantidade = int(request.POST.get('quantidade'))

        if operacao == 'entrada':
            produto.quantidade += quantidade
            produto.save()
            messages.success(request, f'Entrada de {quantidade} unidades realizada com sucesso para o produto {produto.nome}.')
        elif operacao == 'saida':
            if produto.quantidade >= quantidade:
                produto.quantidade -= quantidade
                produto.save()
                messages.success(request, f'Saída de {quantidade} unidades realizada com sucesso para o produto {produto.nome}.')
            else:
                messages.error(request, f'Quantidade insuficiente em estoque para realizar a saída do produto {produto.nome}.')
        else:
            messages.error(request, 'Operação inválida. Selecione "Entrada" ou "Saída".')

        # Registrar a movimentação
        Movimentacao.objects.create(
            tipo=operacao,
            quantidade=quantidade,
            produto=produto
        )

    return redirect('lista_produtos')