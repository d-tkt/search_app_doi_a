from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'パスワードを入力してください。空白は許可されません。'
        self.fields['password2'].help_text = '確認のため、同じパスワードを入力してください。'

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if password1 is None or password1.strip() == '':
            raise ValidationError("パスワードは空白にできません。")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("パスワードが一致しません。")
        if password2 is None or password2.strip() == '':
            raise ValidationError("パスワードは空白にできません。")
        return password2
