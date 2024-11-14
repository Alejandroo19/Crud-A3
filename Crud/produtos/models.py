from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=30)
    ativo = models.BooleanField(default=True)  # Novo campo para indicar se a categoria está ativa

    def __str__(self):
        return self.nome
    
class Produto(models.Model):
    codigo = models.CharField(max_length=10, unique=True, editable=False)
    nome = models.CharField(max_length=60)
    quantidade = models.PositiveIntegerField(default=0, editable=False)
    quantidade_minima = models.PositiveIntegerField(default=0)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        # Se não houver um 'codigo' definido, crie um novo ID sequencial começando em "0001"
        if not self.codigo:
            max_codigo = Produto.objects.aggregate(max=models.Max('codigo'))['max']
            if max_codigo:
                new_codigo = str(int(max_codigo) + 1).zfill(4)
            else:
                new_codigo = '0001'
            self.codigo = new_codigo
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

        
    
class Movimentacao(models.Model):
    tipo = models.CharField(max_length=50)  # Por exemplo, entrada ou saída
    quantidade = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo} - {self.quantidade} ({self.produto.nome})"