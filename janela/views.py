# janela/views.py (COMPLETO E CORRIGIDO)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from janela.forms import PerfilEditForm

# IMPORTANTE: Importamos nosso modelo Usuario e removemos o User padrão
from .models import Usuario, Produto, Carrinho, ItemCarrinho

def index(request):
    return render(request, "janela/index.html")

def menu_inicial(request):
    return render(request, "janela/menu_inicial.html")

def Blog(request):
    return render(request, "janela/Blog.html")

def Curso(request):
    return render(request, "janela/Curso.html")

def contact(request):
    return render(request, "janela/contact.html")

def registro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if not nome or not email or not senha:
            messages.error(request, 'Preencha todos os campos!')
            return redirect('/janela/registro/')
            
        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem!')
            return redirect('/janela/registro/')
            
        # AGORA VERIFICAMOS NO NOSSO MODELO USUARIO
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está cadastrado!')
            return redirect('/janela/registro/')
        
        # AGORA CRIAMOS NO NOSSO MODELO USUARIO
        user = Usuario.objects.create_user(
            username=email, # Django exige um username, usamos o email
            email=email,
            password=senha,
            nome=nome      # Nosso campo customizado
        )
        
        # O sinal post_save já cria o carrinho automaticamente
        
        login(request, user)
        messages.success(request, f'Cadastro realizado! Bem-vindo, {nome}!')
        return redirect('/janela/')

    return render(request, 'janela/registro.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/janela/')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        if not email or not senha:
            messages.error(request, 'Preencha todos os campos!')
            return redirect('/janela/login/')
        
        # O 'authenticate' agora vai usar nosso modelo Usuario por causa do settings.py
        user = authenticate(request, username=email, password=senha)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.nome}!')
            return redirect('/janela/menu_inicial')
        else:
            messages.error(request, 'Email ou senha incorretos!')
    
    return render(request, 'janela/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu com sucesso!')
    return redirect('/janela/menu_inicial')

# As views abaixo já estão corretas e vão funcionar
# pois agora 'request.user' será uma instância de 'Usuario'
@login_required
def perfil(request):
    carrinho = get_object_or_404(Carrinho, usuario=request.user)
    contexto = {
        'carrinho': carrinho,
    }
    return render(request, "janela/perfil.html", contexto)

def ver_produtos(request):
    lista_de_produtos = Produto.objects.all()
    contexto = {
        'produtos': lista_de_produtos
    }
    return render(request, 'janela/products.html', contexto)

@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho = get_object_or_404(Carrinho, usuario=request.user)
    
    item, created = ItemCarrinho.objects.get_or_create(
        carrinho=carrinho,
        produto=produto
    )

    if not created:
        item.quantidade += 1
        item.save()
    
    messages.success(request, f'"{produto.nome}" adicionado ao carrinho!')
    return redirect('/janela/products/')



@login_required
def remover_do_carrinho(request, produto_id):
    # Encontra o item específico no carrinho do usuário logado
    # Buscamos o ItemCarrinho que pertence ao carrinho do usuário E contém o produto específico
    item = get_object_or_404(ItemCarrinho, carrinho__usuario=request.user, produto__id=produto_id)

    # Verifica a quantidade
    if item.quantidade > 1:
        # Se for maior que 1, apenas diminui a quantidade
        item.quantidade -= 1
        item.save()
        messages.info(request, f'Quantidade de "{item.produto.nome}" diminuída no carrinho.')
    else:
        # Se for 1 (ou menos, embora não deva acontecer), remove o item
        nome_produto = item.produto.nome # Guarda o nome antes de deletar
        item.delete()
        messages.success(request, f'"{nome_produto}" removido do carrinho.')

    # Redireciona de volta para a página onde o carrinho é exibido (o perfil)
    return redirect('/janela/perfil/')

@login_required
def perfil(request):
    carrinho = get_object_or_404(Carrinho, usuario=request.user)
    
    if request.method == 'POST':
        form = PerfilEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('/janela/perfil/') 
        else:
            messages.error(request, 'Erro ao atualizar o perfil. Verifique os campos.')
            
    else: 
        form = PerfilEditForm(instance=request.user)

    contexto = {
        'carrinho': carrinho,
        'form': form, 
    }
    return render(request, "janela/perfil.html", contexto)