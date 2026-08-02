from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    

    username = forms.CharField(
        label="ユーザー名"
    )

    email = forms.EmailField(
        label="メールアドレス"
    )

    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="確認用パスワード",
        widget=forms.PasswordInput
    )

    # email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
        
    