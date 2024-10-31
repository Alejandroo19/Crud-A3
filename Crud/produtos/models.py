from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=60)
    quantidade = models.PositiveIntegerField(default=0, editable=False)
    quantidade_minima = models.PositiveIntegerField(default=0)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome