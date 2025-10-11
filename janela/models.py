# seu_app/models.py

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    # NOVO CAMPO DE IMAGEM PARA O PERFIL
    foto_perfil = models.ImageField(upload_to='imagens/', null=True, blank=True)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0)
    # NOVO CAMPO DE IMAGEM PARA O PRODUTO
    imagem = models.ImageField(upload_to='imagens/', null=True, blank=True)

    def __str__(self):
        return self.nome


class Carrinho(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='carrinho')
    criado_em = models.DateTimeField(auto_now_add=True)
    produtos = models.ManyToManyField(Produto, through='ItemCarrinho')

    def __str__(self):
        return f'Carrinho de {self.usuario.nome}'

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens.all())


class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome} no {self.carrinho}'

    @property
    def subtotal(self):
        return self.produto.preco * self.quantidade

    class Meta:
        unique_together = ('carrinho', 'produto')


@receiver(post_save, sender=Usuario)
def criar_ou_atualizar_carrinho_usuario(sender, instance, created, **kwargs):
    if created:
        Carrinho.objects.create(usuario=instance)