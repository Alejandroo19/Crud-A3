from django import forms
from .models import Produto, Categoria
from django.core.validators import MinLengthValidator


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'quantidade_minima', 'preco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade_minima': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

    nome = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[MinLengthValidator(2)], )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].empty_label = "-- Selecione uma Categoria --"
        # Filtro para exibir apenas categorias ativas
        self.fields['categoria'].queryset = Categoria.objects.filter(ativo=True)

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }

        
