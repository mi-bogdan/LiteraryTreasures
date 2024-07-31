<h2 align="center">API интернет магазина книг</h2>


**Ссылки**:
- [VK](https://vk.com/id404101172)
- [Telegram](https://t.me/bogdan_shnyra)


### Описание проекта:
Этот проект представляет собой интернет магазин, разработанный на Django Rest Framework. Он включает в себя следующие возможности:
- Регистрация и авторизация пользователей
- Добавление товаров в корзину и избранное
- Оформление заказа
- Интеграция с платежной системой Юкаса (Yookassa)
- Хранение данных корзины и избранного с использованием Redis
- Оставлять отзыва
- Оставлять свой рейтинг 

### Инструменты разработки

**Стек:**
- Python 
- Django rest framework
- PostgreSQL
- Docker
- Redis
- Yookassa API

## Разработка

##### 1) Клонировать репозиторий

    git clone https://github.com/mi-bogdan/LiteraryTreasures.git

##### 2) Создать виртуальное окружение

    python -m venv venv
    
##### 3) Активировать виртуальное окружение

    venv/Scripts/activate       

##### 4) Устанавливить зависимости:

    pip install -r requirements.txt

##### 6) Выполнить команду для выполнения миграций

    python manage.py migrate
    
##### 8) Создать суперпользователя

    python manage.py createsuperuser
    
##### 9) Запустить сервер

    python manage.py runserver

После этого API объявлений будет доступен по адресу http://localhost:8000/.

### Библиотека
**Ссылки**:
- [Yookasa] https://yookassa.ru/my/merchant/integration/http-notifications
- [ngrok] https://ngrok.com/
- [Github-Yookasa]https://github.com/yoomoney/yookassa-sdk-python




Copyright (c) 2024-present, - Shnyra Bogdan