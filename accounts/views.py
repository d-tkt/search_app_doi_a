from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"ようこそ、{username}さん。")
                return redirect('search')  # ログイン後のリダイレクト先
            else:
                messages.error(request, "ユーザー名またはパスワードが間違っています。")
        else:
            messages.error(request, "ユーザー名またはパスワードが間違っています。")
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "ログアウトしました。")
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('search')  # または適切なリダイレクト先
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
