from django.shortcuts import render
from django.contrib import messages

def index(request):
    data = {
        'title': 'Главная страница',
    }
    return render(request, 'main/index.html', data)

def about(request):
    return render(request, 'main/about.html')

def contacts(request):
    contacts_data = [
        {'name': 'Богдан', 'role': 'Администратор', 'email': 'bogdanvolkov2017@yandex.ru'},
    ]
    sent = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        messages.success(request, f'Сообщение от {name} ({email}) отправлено!')
        sent = True
    return render(request, 'main/contacts.html', {'contacts': contacts_data, 'sent': sent})