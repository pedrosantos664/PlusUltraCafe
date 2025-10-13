# janela/admin.py
from django.contrib import admin
from .models import Usuario, Produto, Carrinho, ItemCarrinho

# Customização para o seu modelo Usuario (usando ModelAdmin)
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # Mostra estes campos na lista de usuários
    list_display = ('nome', 'email', 'foto_perfil')
    # Adiciona uma barra de busca
    search_fields = ('nome', 'email')

# Customização para o modelo Produto
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque', 'imagem')
    search_fields = ('nome',)
    list_filter = ('preco', 'estoque')

# Permite ver os itens do carrinho dentro da página do próprio carrinho
class ItemCarrinhoInline(admin.TabularInline):
    model = ItemCarrinho
    extra = 1 # Quantos campos de item extra mostrar

@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'criado_em', 'total')
    # Adiciona a tabela de itens na página de detalhes do carrinho
    inlines = [ItemCarrinhoInline]

# Não precisamos mais registrar ItemCarrinho separadamente,
# pois ele já é gerenciado dentro do CarrinhoAdmin.
# admin.site.register(ItemCarrinho)