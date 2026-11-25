# Savora: устройство проекта

Savora — Django-приложение для поиска ресторанов, бронирования столиков,
отзывов и избранного. База данных — SQLite.

## Структура

```text
foodcort/
├── manage.py                 # команды Django
├── requirements.txt          # зависимости
├── .env                      # локальный SECRET_KEY, исключён из Git
├── .env.example              # пример настроек окружения
├── db.sqlite3                # локальная база данных
├── my_project/
│   ├── settings.py           # настройки, база, шаблоны, статика
│   ├── urls.py               # корневые маршруты
│   ├── asgi.py
│   └── wsgi.py
└── my_one_app/
    ├── models.py             # структура данных
    ├── views.py              # обработка запросов
    ├── urls.py               # маршруты приложения
    ├── admin.py              # административный интерфейс
    ├── migrations/           # история схемы и начальные данные
    ├── templates/            # HTML-шаблоны
    └── static/               # CSS и изображения
```

## Исправленная ошибка SECRET_KEY

Ошибка `The SECRET_KEY setting must not be empty` возникала потому, что
`dotenv.get_key('.env', 'SECRET_KEY')` возвращал пустое значение при отсутствии
локального файла. Django падал при создании подписи cookie в middleware сообщений.

Теперь `.env` загружается относительно корня проекта, а переменная окружения
`SECRET_KEY` имеет приоритет. При отсутствии или пустом ключе запуск сразу
останавливается с понятной инструкцией. Локальный `.env` создан с уникальным
ключом; публиковать его в Git не нужно.

При новом клонировании создайте ключ из корня проекта:

```powershell
.\.venv\Scripts\python.exe -c "from pathlib import Path; from django.core.management.utils import get_random_secret_key; p = Path('.env'); p.exists() or p.write_text('SECRET_KEY=' + get_random_secret_key() + '\n', encoding='utf-8')"
```

Команда сохраняет существующий `.env` без изменений. Если файл уже существует,
но ключ в нём отсутствует, добавьте `SECRET_KEY` вручную по примеру `.env.example`.

## Models — my_one_app/models.py

### Restaurant — ресторан

| Поле | Назначение |
| --- | --- |
| `name` | Название, до 120 символов |
| `slug` | Уникальный идентификатор для URL |
| `cuisine`, `location` | Кухня и район/местоположение, до 80 символов |
| `price` | Ценовая категория, до 5 символов |
| `description` | Описание |
| `image_class` | CSS-класс изображения, по умолчанию `food1` |
| `image` | Необязательное изображение в `media/restaurants/` |
| `rating` | Рейтинг: десятичное число с одним знаком после запятой |
| `latitude`, `longitude` | Координаты, 6 знаков после запятой |

Сортировка: рейтинг по убыванию, затем название. `get_absolute_url()` возвращает
адрес `restaurant_detail` по `slug`. Рейтинг хранится отдельно и автоматически
по отзывам не пересчитывается.

### Review — отзыв

`restaurant` связывает отзыв с рестораном, `user` — с необязательным автором
из `auth.User`. Дополнительно хранятся `author` (имя), `role`, `score`
(десятичная оценка с одним знаком после запятой), `text`.
Обработчики принимают оценки от 0 до 10. Обратные связи:
`restaurant.reviews` и `user.restaurant_reviews`.
Удаление связанного ресторана или пользователя удаляет связанные отзывы (`CASCADE`).

### Favorite — избранное

Поля: `user`, `restaurant`, `created_at` (время создания).
Ограничение `unique_user_restaurant_favorite` запрещает повтор одной пары
пользователь–ресторан. Обратные связи: `user.favorite_restaurants` и
`restaurant.favorites`. Удаление пользователя или ресторана удаляет запись.

### Reservation — бронирование

Поля: `restaurant`, `date`, `time`, `guests` (по умолчанию 2), `created_at`.
Сортировка по дате и времени. Обратная связь: `restaurant.reservations`.
Форма принимает от 1 до 20 гостей. У бронирования нет связи с пользователем;
его может создать и гость сайта. Удаление ресторана удаляет бронирования.

## Views и URLs

`my_project/urls.py` подключает административный интерфейс по `/admin/`
и все маршруты `my_one_app/urls.py` от корня сайта. При `DEBUG=True`
добавляется раздача файлов `/media/` из `MEDIA_ROOT`.

| URL | Имя маршрута | View | Поведение |
| --- | --- | --- | --- |
| `/` | `home` | `home` | Главная, шаблон `index.html` |
| `/restaurants/` | `restaurants` | `restaurants` | Каталог, шаблон `restaurants.html` |
| `/restaurant/` | `restaurant` | `restaurant` | Страница ресторана со slug `hearth-co` |
| `/restaurant/<slug>/` | `restaurant_detail` | `restaurant` | Карточка ресторана, отзывы, POST бронирования; `restaurant.html` |
| `/profile/` | `profile` | `profile` | Шаблон `profile.html`, вход не обязателен |
| `/article/` | `article` | `article` | Журнал, шаблон `article.html` |
| `/login/` | `login` | `login_view` | `AuthenticationForm`, вход по POST, переход на `next` или профиль |
| `/register/` | `register` | `register` | `UserCreationForm`, создание пользователя по POST и автоматический вход |
| `/logout/` | `logout` | `logout_view` | Выход по POST, переход на главную |
| `/restaurant/<slug>/favorite/` | `toggle_favorite` | `toggle_favorite` | Вход обязателен; POST добавляет/убирает избранное |
| `/restaurant/<slug>/reviews/add/` | `create_review` | `create_review` | Вход обязателен; POST создаёт отзыв |
| `/reviews/<review_id>/edit/` | `edit_review` | `edit_review` | Вход обязателен; POST меняет только собственный отзыв |
| `/reviews/<review_id>/delete/` | `delete_review` | `delete_review` | Вход обязателен; POST удаляет только собственный отзыв |

Каталог принимает параметры GET: `q` (поиск по названию, кухне и локации),
`cuisine` (частичное совпадение), `price` (точное совпадение), `location`
(точное совпадение без учёта регистра), `rating` (минимальный рейтинг), `page`.
Пагинация — 3 ресторана на страницу с сохранением фильтров.

Карточка ресторана проверяет дату, время и число гостей при POST и сохраняет
`Reservation`. После отправки выводит результат в том же шаблоне.
Операции с избранным и отзывами возвращают пользователя на карточку ресторана.
Несуществующий ресторан или чужой отзыв при редактировании/удалении дают 404.
Некорректный текст/оценка отзыва игнорируются без сообщения об ошибке.
Шаблоны входа и регистрации находятся в `templates/registration/`.

## Локальный запуск в PowerShell

Команды выполняются из папки с `manage.py`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
# При первом клонировании создайте .env по инструкции выше.
python manage.py migrate
python manage.py check
python manage.py runserver
```

Открыть: http://127.0.0.1:8000/. Для административного интерфейса:
`python manage.py createsuperuser`. Текущий `DEBUG=True` предназначен для
локальной разработки.
