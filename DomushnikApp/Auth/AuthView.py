from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views import View
from .forms import RegisterForm, LoginForm

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'auth/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Перенаправляем на страницу входа
        # Если форма не валидна, возвращаем шаблон с ошибками
        return render(request, 'auth/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Перенаправляем на домашнюю страницу
        # Если форма не валидна, возвращаем шаблон с формой и ошибками
        return render(request, 'auth/login.html', {'form': form})

