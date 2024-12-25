from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegister
from .models import *

# Create your views here.


def platform(request):
    title = "Главная страница"
    context = {
        'title': title,
    }
    return render(request, 'platform.html', context)


def games(request):
    title = "Игры"
    games = Game.objects.all()
    buy = "Купить"
    context = {
        'title': title,
        'games': games,
        'buy': buy,
    }
    return render(request, 'games.html', context)


def cart(request):
    title = "Корзина"
    img = "/static/Корзина.jpg"
    text_1 = "Здесь"
    text_2 = "ничего"
    text_3 = "НЕТ!"
    context = {
        'title': title,
        'img': img,
        'text_1': text_1,
        'text_2': text_2,
        'text_3': text_3,
    }
    return render(request, 'cart.html', context)

# Теперь уже ненужный список...
# users = ["Sergey", "Dmitriy", "Maria", "Polina"]


def sign_up_by_django(request):
    users = Buyer.objects.all().values_list('name', flat=True)
    info = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            # Получение данных:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            if username in users:
                error = 'Пользователь уже существует'
                info['ошибка'] = error
                for key, value in info.items():
                    if value == error:
                        return HttpResponse(f'{key}: {value}')
            elif password != repeat_password:
                error = 'Пароли не совпадают'
                info['ошибка'] = error
                for key, value in info.items():
                    if value == error:
                        return HttpResponse(f'{key}: {value}')
            elif age < 18:
                error = 'Вы должны быть старше 18'
                info['ошибка'] = error
                for key, value in info.items():
                    if value == error:
                        return HttpResponse(f'{key}: {value}')
            else:
                Buyer.objects.create(name=username,
                                     age=age)
                return HttpResponse(f'Приветствуем, {username}!')
    else:
        form = UserRegister()
        context = {
            'info': info,
            'form': form,
        }
        return render(request, 'registration_page.html', context)
