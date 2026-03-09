# СТАРТ — сайт продажи энергетиков

> В этой версии фронт заметно переделан под макет. Если в браузере вдруг виден старый стиль, нажми **Ctrl+F5** или перезапусти контейнеры через `docker compose down -v && docker compose up --build`.

Готовый Django-проект для локального запуска на Windows 10 через Docker Desktop и Docker Compose.

## Что уже есть

- главная страница с большой банкой и кнопкой **«ЗАБРАТЬ ЗАРЯД»**
- страница каталога с 4 энергетиками
- адаптивная вёрстка для компьютера и смартфона
- PostgreSQL в Docker Compose
- Django Admin, где можно менять:
  - картинку товара
  - название вкуса
  - цену
  - количество в наличии
  - порядок вывода
  - активность товара

## Стек

- Python 3.12
- Django 5
- PostgreSQL 16
- Docker / Docker Compose

## Как запустить

### 1. Распакуй архив
Например в папку:

```bash
C:\projects\start_energy_shop
```

### 2. Создай файл `.env`
Скопируй `.env.example` в `.env`

Пример для локального запуска:

```env
SECRET_KEY=django-insecure-change-me
DEBUG=1
ALLOWED_HOSTS=127.0.0.1,localhost
POSTGRES_DB=start_energy
POSTGRES_USER=start_user
POSTGRES_PASSWORD=start_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 3. Открой проект в PyCharm

### 4. Запусти контейнеры
Из корня проекта:

```bash
docker compose up --build
```

Сайт будет доступен по адресу:

```bash
http://127.0.0.1:8000/
```

## Админка

Чтобы создать администратора, в новом терминале выполни:

```bash
docker compose exec web python manage.py createsuperuser
```

Админка:

```bash
http://127.0.0.1:8000/admin/
```

## Как менять товары

Открой админку и зайди в раздел **Products**.

У каждого товара можно менять:

- `name` — название продукта
- `flavor` — вкус
- `price` — цена
- `stock` — остаток на складе
- `image` — картинка банки
- `is_active` — показывать или скрывать товар
- `sort_order` — порядок карточек в каталоге
- `hero_product` — сделать банку главной на первом экране

## Полезно знать

- При первом запуске проект сам создаёт 4 демо-товара.
- Команда заполнения тестовыми данными не создаёт дубликаты.
- Картинки лежат в папке `media/products/`.
- Для реального продакшена позже можно добавить Nginx, Gunicorn, корзину и оформление заказа.

## Остановка

```bash
docker compose down
```

## Сброс базы

Если захочешь начать с чистого листа:

```bash
docker compose down -v
docker compose up --build
```
