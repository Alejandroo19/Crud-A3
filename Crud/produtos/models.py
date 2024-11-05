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
        
    
class Movimentacao(models.Model):
    # Defina os campos do modelo Movimentacao de acordo com as suas necessidades
    tipo = models.CharField(max_length=50)  # Por exemplo, entrada ou saída
    quantidade = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)
    # Outros campos que você precisar

    def __str__(self):
        return f"{self.tipo} - {self.quantidade}"