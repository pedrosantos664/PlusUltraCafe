from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from janela.models import Usuario

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'form-input',
            'placeholder': _('seu@email.com')
        })
    )
    password = forms.CharField(
        label=_("Senha"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-input',
            'placeholder': _('Sua senha')
        })
    )

    error_messages = {
        'invalid_login': _(
            "Por favor, insira um email e senha corretos. Note que ambos "
            "os campos diferenciam maiúsculas e minúsculas."
        ),
        'inactive': _("Esta conta está inativa."),
    }


class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': _('seu@email.com')
        }),
        help_text=_("Obrigatório. Insira um endereço de email válido.")
    )
    
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': _('Seu nome')
        }),
        max_length=30,
        help_text=_("Obrigatório. Máximo de 30 caracteres.")
    )

    password1 = forms.CharField(
        label=_("Senha"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': _('Crie uma senha segura')
        }),
        help_text=_(
            "Sua senha deve conter pelo menos 8 caracteres, "
            "não pode ser muito comum e não pode ser inteiramente numérica."
        )
    )
    
    password2 = forms.CharField(
        label=_("Confirmação de senha"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': _('Repita a mesma senha')
        }),
        help_text=_("Digite a mesma senha novamente para verificação.")
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Este email já está em uso."))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Para compatibilidade
        if commit:
            user.save()
        return user
    



class PerfilEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # Liste APENAS os campos que o usuário pode editar
        fields = ['nome', 'email', 'foto_perfil'] 
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Seu nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Seu melhor email'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-input-file'}),
        }
        labels = {
            'nome': 'Nome Completo',
            'email': 'Endereço de Email',
            'foto_perfil': 'Foto de Perfil (Opcional)',
        }

    # Validação extra para garantir que o novo email (se alterado) não esteja em uso por OUTRO usuário
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # 'self.instance' é o objeto Usuario que está sendo editado
        if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este endereço de email já está em uso por outro usuário.")
        return email 