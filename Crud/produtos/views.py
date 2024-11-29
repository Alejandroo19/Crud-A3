# views.py
from django.shortcuts import render, redirect, get_object_or_404 
from .models import Produto, Categoria, Movimentacao
from .forms import ProdutoForm, CategoriaForm
from django.contrib import messages 
from django.db import models 
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse

def lista_produtos(request):
    # Filtra apenas os produtos ativos para a tela inicial
    produtos = Produto.objects.filter(ativo=True)
    
    categorias_ativas = Categoria.objects.filter(ativo=True)

    # Debug - Verificar categorias ativas
    print("Categorias ativas (na view):", categorias_ativas)

    # Verificar se há produtos com estoque abaixo do mínimo e que estejam ativos
    produtos_estoque_baixo = Produto.objects.filter(quantidade__lte=models.F('quantidade_minima'), ativo=True)
    tem_estoque_baixo = produtos_estoque_baixo.exists()

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

    # Passar as categorias e a flag `tem_estoque_baixo` para o contexto
    return render(request, 'produtos/lista_produtos.html', {
        'produtos': produtos,
        'form': form,
        'categorias': categorias_ativas,  # Incluindo as categorias no contexto
        'tem_estoque_baixo': tem_estoque_baixo  # Para controle da mensagem de aviso
    })
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
def estoque_baixo(request):
    # Filtrar produtos com quantidade menor do que a quantidade mínima
    produtos = Produto.objects.filter(quantidade__lt=models.F('quantidade_minima'))
    
    # Obter apenas categorias ativas para serem usadas no formulário de cadastro/procura
    categorias_ativas = Categoria.objects.filter(ativo=True)

    # Renderizar o template principal, passando o queryset dos produtos filtrados
    return render(request, 'produtos/lista_produtos.html', {
        'produtos': produtos,
        'categorias': categorias_ativas,
        'form': ProdutoForm(),
    })

# Procurar produto


def procurar_produto(request):
    nome = request.GET.get('nome', '').strip()
    codigo = request.GET.get('codigo', '').strip()
    categoria_id = request.GET.get('categoria', '').strip()
    incluir_ativos = request.GET.get('incluir_ativos') == 'on'
    incluir_inativos = request.GET.get('incluir_inativos') == 'on'
    incluir_estoque_baixo = request.GET.get('incluir_estoque_baixo') == 'on'

    # Inicia o queryset de produtos
    produtos = Produto.objects.all()

    # Filtra pelo nome, se informado
    if nome:
        produtos = produtos.filter(nome__icontains=nome)

    # Filtra pelo código, se informado
    if codigo:
        produtos = produtos.filter(codigo__icontains=codigo)

    # Filtra pela categoria, se selecionada
    if categoria_id and categoria_id != "Todas":
        produtos = produtos.filter(categoria_id=categoria_id)

    # Filtros combinados
    query = Q()  # Cria uma query vazia para acumular condições

    if incluir_ativos:
        query |= Q(ativo=True)

    if incluir_inativos:
        query |= Q(ativo=False)

    if incluir_estoque_baixo:
        # Inclui apenas produtos ativos com estoque baixo
        query |= Q(ativo=True, quantidade__lte=models.F('quantidade_minima'))

    # Aplica os filtros combinados ao queryset
    if query:
        produtos = produtos.filter(query)

    # Cria uma instância do ProdutoForm e atualiza o queryset das categorias
    categorias = Categoria.objects.filter(ativo=True)  # Certificar que apenas categorias ativas são exibidas
    form = ProdutoForm()
    form.fields['categoria'].queryset = categorias

    return render(request, 'produtos/lista_produtos.html', {
        'produtos': produtos,
        'form': form,
        'categorias': categorias
    })

# editar produto
def editar_produto(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    categorias = Categoria.objects.filter(ativo=True)
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('lista_produtos')
        else:
            messages.error(request, 'Erro ao atualizar produto.')
    else:
        form = ProdutoForm(instance=produto)
        form.fields['categoria'].queryset = categorias

    produtos = Produto.objects.all()

    return render(request, 'produtos/editar_produto.html', {
        'form': form,
        'produto': produto,  # Passa o produto para verificar se está ativo ou não
        'categorias': categorias
    })

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
        try:
            # Converter a quantidade para int e verificar se é válida
            quantidade = int(request.POST.get('quantidade'))

            # Limite máximo que pode ser suportado (baseado na capacidade do banco)
            max_quantidade = 99999999999999999
            if quantidade > max_quantidade:
                raise ValidationError("A quantidade não pode ser maior que 99999.")
            
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
            
            # Verificar se a quantidade está agora acima da quantidade mínima, para remover o aviso "Estoque Baixo"
            if produto.quantidade >= produto.quantidade_minima:
                messages.info(request, f'O produto {produto.nome} agora está acima da quantidade mínima.')

        except ValueError:
            messages.error(request, "Por favor, insira uma quantidade válida.")
        except ValidationError as e:
            messages.error(request, str(e))

    return redirect('lista_produtos')
    

def ativar_desativar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    produto.ativo = not produto.ativo  # Alterna entre ativo e inativo
    produto.save()
    
    if produto.ativo:
        messages.success(request, f'O produto "{produto.nome}" foi reativado com sucesso.')
    else:
        messages.success(request, f'O produto "{produto.nome}" foi desativado com sucesso.')
        
    return redirect('lista_produtos')