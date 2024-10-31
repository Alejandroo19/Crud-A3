# entradas/forms.py
from django import forms
from .models import Movimentacao
from produtos.models import Produto

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['produto', 'data', 'quantidade', 'tipo']

    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']
        tipo = self.cleaned_data.get('tipo')
        produto = self.cleaned_data.get('produto')
        
        # Verifique se o tipo é "saída" e a quantidade é válida
        if tipo == 'saida' and produto and quantidade > produto.quantidade:
            raise forms.ValidationError("Quantidade de saída maior que o estoque disponível.")
        return quantidade
