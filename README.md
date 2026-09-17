# Savora

## Описание проекта

Savora — это веб-приложение для поиска ресторанов и чтения гастрономического журнала. Пользователь может найти ресторан по названию, кухне, рейтингу или локации, открыть его персональную страницу, посмотреть карту, забронировать столик и добавить место в избранное. Зарегистрированные пользователи также могут оставлять, редактировать и удалять собственные комментарии.

Проект адаптирован для desktop и mobile, поддерживает переключение русского и английского языка, светлую и тёмную тему, пагинацию каталога и интерактивные accordion-карточки отзывов.

Savora is a Django culinary journal and restaurant discovery app. It includes a searchable restaurant catalog, restaurant detail pages, reservations, user reviews, favorites, authentication, responsive mobile/desktop layouts, theme switching, language switching, pagination, and OpenStreetMap locations.

## Stack

- Python 3.13+
- Django 6.1.1
- SQLite
- HTML templates and CSS
- OpenStreetMap embeds for restaurant maps

## Project Structure

```text
foodCort__project/
|-- requirements.txt
|-- .venv/
|-- README.md
`-- my_project/
    |-- manage.py
    |-- db.sqlite3
    |-- my_project/
    |   |-- settings.py
    |   |-- urls.py
    |   |-- asgi.py
    |   `-- wsgi.py
    `-- my_one_app/
        |-- models.py
        |-- views.py
        |-- urls.py
        |-- admin.py
        |-- migrations/
        |-- templates/
        `-- static/style.css
```

## Setup on Windows

Open PowerShell in the project root:

```powershell
cd C:\Users\Asus\Desktop\foodCort__project
.\.venv\Scripts\Activate.ps1
```

If the virtual environment does not exist, create it and install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Apply migrations:

```powershell
cd my_project
python manage.py migrate
```

Start the development server:

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/ in a browser.

## Useful Commands

Run Django checks:

```powershell
python manage.py check
```

Create a new migration after changing models:

```powershell
python manage.py makemigrations
python manage.py migrate
```

Create an administrator:

```powershell
python manage.py createsuperuser
```

Admin panel:

http://127.0.0.1:8000/admin/

## Main Pages

| URL | Description |
| --- | --- |
| `/` | Home page with search and featured content |
| `/restaurants/` | Restaurant catalog with pagination, search, and filters |
| `/restaurant/<slug>/` | Restaurant detail page |
| `/profile/` | User profile and preferences |
| `/article/` | Critics' journal and reading list page |
| `/login/` | Login |
| `/register/` | Registration |
| `/admin/` | Django administration |

## Features

### Restaurant catalog

The catalog supports:

- Search by restaurant name, cuisine, or location using `?q=`.
- Filters for cuisine, price, rating, and location.
- Three restaurants per page with query-preserving pagination.
- Separate detail pages for every restaurant using a unique slug.
- Coordinate links and OpenStreetMap embeds.

Examples:

```text
/restaurants/?q=japanese
/restaurants/?cuisine=French
/restaurants/?price=$$$$
/restaurants/?rating=4.8
/restaurants/?location=Soho
```

### User accounts

Registered users can:

- Log in and log out.
- Add or remove restaurants from favorites.
- Publish comments on restaurant detail pages.
- Edit and delete their own comments only.
- Switch between English and Russian.
- Switch between light and dark themes.

### Reservations

Restaurant detail pages contain mobile and desktop reservation forms. Valid reservations are stored in the `Reservation` model with a restaurant, date, time, and guest count.

### Models

- `Restaurant`: catalog data, rating, location, and coordinates.
- `Review`: restaurant reviews and optional user ownership.
- `Favorite`: unique user-to-restaurant favorites.
- `Reservation`: restaurant booking requests.

## Database

The project uses SQLite at `my_project/db.sqlite3`. Initial restaurant and review data is loaded by the first app migration. Coordinates are populated by the second migration.

## Frontend Notes

- Desktop content uses the `desktop-only` layout.
- Mobile content uses the `mobile-view` layout.
- Language and theme preferences are stored in `localStorage`.
- Restaurant reviews use collapsible accordion cards on mobile and desktop.
- Maps use OpenStreetMap embed URLs and do not require an API key.

## Troubleshooting

If Django cannot be imported, activate the virtual environment or use its interpreter directly:

```powershell
..\.venv\Scripts\python.exe manage.py check
```

If the database is out of date:

```powershell
python manage.py migrate
```

If the browser shows stale CSS or JavaScript, refresh the page with `Ctrl+F5` while the development server is running.
