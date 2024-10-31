# entradas/views.py
from django.shortcuts import render, redirect
from .forms import MovimentacaoForm
from produtos.models import Produto

def movimentar_produto(request):
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            produto = movimentacao.produto

            # Atualizar a quantidade do produto
            if movimentacao.tipo == 'entrada':
                produto.quantidade += movimentacao.quantidade
            elif movimentacao.tipo == 'saida':
                produto.quantidade -= movimentacao.quantidade

            produto.save()
            movimentacao.save()
            return redirect('lista_produtos')
    else:
        form = MovimentacaoForm()
    
    return render(request, 'saidas/movimentar_produto.html', {'form': form})
