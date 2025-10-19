# janela/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Produto, Carrinho, ItemCarrinho, Usuario 

User = get_user_model()

# Desregistra o admin padrão (se necessário)
admin.site.unregister(User)

# Registra com customização
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'is_staff')


admin.site.register(Produto)
admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)
