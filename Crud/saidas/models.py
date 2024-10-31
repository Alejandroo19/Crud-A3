# saidas/models.py
from django.db import models
from produtos.models import Produto

class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='saidas_movimentacoes')
    data = models.DateField()
    quantidade = models.PositiveIntegerField()
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)

    def __str__(self):
        return f'{self.tipo} - {self.produto.nome}'
