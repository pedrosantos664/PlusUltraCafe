# janela/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# 1. HERDAR DE ABSTRACTUSER
class Usuario(AbstractUser):
    # AbstractUser já tem: username, email, password, first_name, last_name, etc.
    # Vamos adicionar nosso campo 'nome' e tornar o email o campo de login.
    
    nome = models.CharField(max_length=150, blank=True)
    # Sobrescrevemos o email para garantir que seja único
    email = models.EmailField(unique=True)
    foto_perfil = models.ImageField(upload_to='media/', null=True, blank=True)

    # 2. DEFINIR OS CAMPOS OBRIGATÓRIOS DO DJANGO
    # Diz ao Django para usar o email para o login em vez do username
    USERNAME_FIELD = 'email'
    # Campos que serão pedidos ao criar um superusuário (além de email e senha)
    REQUIRED_FIELDS = ['username', 'nome']

    def __str__(self):
        return self.email


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0)
    imagem = models.ImageField(upload_to='fotosprodutos/', null=True, blank=True)

    def __str__(self):
        return self.nome


class Carrinho(models.Model):
    # O OneToOneField agora aponta para o modelo de usuário definido em settings.py
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carrinho')
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

    class Meta:
        unique_together = ('carrinho', 'produto')
        
    @property
    def subtotal(self):
        return self.produto.preco * self.quantidade

    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome}'


# O 'sender' agora aponta para o modelo de usuário correto
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def criar_carrinho_para_novo_usuario(sender, instance, created, **kwargs):
    if created:
        Carrinho.objects.create(usuario=instance)