from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import RegisterUserForm, LoginUserForm, ProfileForm, PasswordChangeCustomForm
from django.contrib import messages
from .models import UserProfile
from django.utils import timezone

@login_required
def profile_view(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        password_form = PasswordChangeCustomForm(request.user, request.POST)
        if 'avatar_submit' in request.POST and profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Аватар успешно обновлен!')
            return redirect('profile')
        elif 'password_submit' in request.POST and password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        password_form = PasswordChangeCustomForm(request.user)

    return render(request, 'register/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })

def register_view(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='reader')
            login(request, user)
            messages.success(request, f'Аккаунт создан для {user.username}! Вы вошли в систему.')
            response = redirect('news_home')
            response.set_cookie('last_login', timezone.now().strftime('%Y-%m-%d %H:%M:%S'), max_age=3600*24*30)
            return response
        else:
            messages.error(request, 'Ошибка при регистрации. Проверьте введенные данные.')
    else:
        form = RegisterUserForm()
    return render(request, 'register/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            response = redirect('news_home')
            response.set_cookie('last_login', timezone.now().strftime('%Y-%m-%d %H:%M:%S'), max_age=3600*24*30)
            return response
        else:
            messages.error(request, 'Ошибка входа. Неверное имя пользователя или пароль.')
    else:
        form = LoginUserForm()
    return render(request, 'register/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    response = redirect('home')
    response.set_cookie('last_logout', timezone.now().strftime('%Y-%m-%d %H:%M:%S'), max_age=3600*24*30)
    return response