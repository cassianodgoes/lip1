import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(senha):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(senha):
        raise ValidationError((
            'Pelo menos uma letra maiuscula, uma minúscula, um número e precisa ter ao menos oito caracteres.'
        ),
            code='Invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu usuário')
        add_placeholder(self.fields['email'], 'Seu e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: José')
        add_placeholder(self.fields['last_name'], 'Ex.: Neto')
        add_attr(self.fields['username'], 'css', 'a-css-class')

    senha = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Sua senha'
        }),
        error_messages={
            'required': 'Senha não pode ficar vazia'
        },
        help_text=(
            'Pelo menos uma letra maiuscula, uma minúscula, um número e precisa ter ao menos oito caracteres.'
        ),
        validators=[strong_password]
    )
    senha2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita sua senha'
        }),
        validators=[strong_password]
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]
        # exclude = ['first_name']
        labels = {
            'username': 'Usuário',
            'first_name': 'Primeiro nome',
            'last_name': 'Último nome',
            'email': 'E-mail',
        }
        help_texts = {
            'email': 'O e-mail precisa ser válido',
        }
        error_messages = {
            'username': {
                'required': 'Esse campo não pode ficar vazio',
            }
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid',
            )

        return email
