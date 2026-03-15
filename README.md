# СТАРТ — сайт продажи энергетиков

Теперь в проект добавлен **production-деплой через GitHub Actions + Docker Compose + Caddy** для домена:

- `sharashkinakontora.shop`
- `www.sharashkinakontora.shop`

## Что есть теперь

- локальный запуск через `docker compose up --build`
- production-запуск через `docker-compose.prod.yml`
- автоматический деплой по `git push` в `main` или `master`
- проксирование домена и HTTPS через **Caddy**
- PostgreSQL в отдельном контейнере
- Gunicorn для Django
- автоматические миграции и `collectstatic`
- автоматическое создание админа, если заполнены переменные `DJANGO_SUPERUSER_*`

---

## 1. Что нужно на сервере

Нужен VPS / сервер с Ubuntu и публичным IP.

На сервере должны быть установлены:

- Docker Engine
- Docker Compose plugin

Пример базовой подготовки сервера:

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
```

Потом перелогинься на сервер и проверь:

```bash
docker --version
docker compose version
```

---

## 2. DNS для домена

У регистратора домена создай записи:

- `A` для `@` → IP твоего сервера
- `A` для `www` → IP твоего сервера

После обновления DNS домен должен открываться на сервер.

Важно: для автоматического HTTPS должны быть открыты порты:

- `80`
- `443`

Если на сервере включён firewall, открой их:

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

---

## 3. Какие GitHub secrets добавить

В GitHub открой:

`Repository -> Settings -> Secrets and variables -> Actions`

И создай secrets:

### `SSH_HOST`
IP адрес сервера

Пример:

```text
123.123.123.123
```

### `SSH_PORT`
Обычно:

```text
22
```

### `SSH_USER`
Пользователь сервера

Пример:

```text
root
```

или

```text
ubuntu
```

### `SSH_PRIVATE_KEY`
Приватный SSH-ключ, которым GitHub Actions будет входить на сервер.

Обычно это содержимое файла:

```text
~/.ssh/id_ed25519
```

### `SSH_KNOWN_HOSTS`
Хост-ключ сервера.

На своём компьютере можно получить так:

```bash
ssh-keyscan -H sharashkinakontora.shop
```

или так:

```bash
ssh-keyscan -H 123.123.123.123
```

Весь вывод вставь в secret целиком.

### `DEPLOY_PATH`
Папка проекта на сервере.

Пример:

```text
/opt/energy_2
```

### `DJANGO_ENV_FILE`
Это **весь текст production `.env` файла**, вставленный в secret целиком.

Готовый пример:

```env
SECRET_KEY=django-insecure-change-me-very-long-production-key
DEBUG=0
ALLOWED_HOSTS=sharashkinakontora.shop,www.sharashkinakontora.shop
CSRF_TRUSTED_ORIGINS=https://sharashkinakontora.shop,https://www.sharashkinakontora.shop
POSTGRES_DB=start_energy
POSTGRES_USER=start_user
POSTGRES_PASSWORD=super-strong-password
POSTGRES_HOST=db
POSTGRES_PORT=5432
FORCE_HTTPS=1
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@sharashkinakontora.shop
DJANGO_SUPERUSER_PASSWORD=replace-this-password-now
```

---

## 4. Как подготовить SSH-ключ

Если ключа ещё нет, на своём компьютере создай его:

```bash
ssh-keygen -t ed25519 -C "github-actions-deploy"
```

Потом:

- **публичный ключ** (`id_ed25519.pub`) добавь на сервер в `~/.ssh/authorized_keys`
- **приватный ключ** (`id_ed25519`) вставь в GitHub secret `SSH_PRIVATE_KEY`

Если заходишь под `root`:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Вставь туда содержимое `id_ed25519.pub`.

---

## 5. Первый запуск вручную на сервере

GitHub Actions сам создаст папку и всё зальёт, но лучше один раз подготовить каталог:

```bash
mkdir -p /opt/energy_2
```

Если пользователь не в группе docker, временно можно запускать через `sudo`, но лучше сразу выдать права через группу docker.

---

## 6. Как работает деплой

После `git push` в `main` или `master` GitHub Actions:

1. подключается к серверу по SSH
2. копирует проект в папку `DEPLOY_PATH`
3. записывает `.env` из секрета `DJANGO_ENV_FILE`
4. выполняет:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

---

## 7. Что смотреть на сервере, если что-то не так

Логи контейнеров:

```bash
cd /opt/energy_2
docker compose -f docker-compose.prod.yml logs -f
```

Статус контейнеров:

```bash
docker compose -f docker-compose.prod.yml ps
```

Перезапуск:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

Остановка:

```bash
docker compose -f docker-compose.prod.yml down
```

---

## 8. Локальный запуск как раньше

Для локальной разработки оставлен обычный файл:

```bash
docker compose up --build
```

Пример локального `.env`:

```env
SECRET_KEY=django-insecure-change-me
DEBUG=1
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000
POSTGRES_DB=start_energy
POSTGRES_USER=start_user
POSTGRES_PASSWORD=start_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
FORCE_HTTPS=0
```

---

## 9. Важный момент по картинкам товаров

В production добавлен постоянный том для `media`, чтобы загруженные картинки не пропадали при деплое.

При первом запуске проект автоматически копирует стартовые изображения из проекта в volume.

---

## 10. Файлы, которые добавлены для продакшена

- `.github/workflows/deploy.yml`
- `docker-compose.prod.yml`
- `Caddyfile`
- `entrypoint.prod.sh`
- `.dockerignore`

---

## 11. Что делать дальше

1. Загрузи проект в GitHub
2. Добавь secrets
3. Настрой DNS домена на IP сервера
4. Сделай `git push`
5. Подожди, пока workflow завершится
6. Открой:
   - `https://sharashkinakontora.shop`
   - `https://www.sharashkinakontora.shop`

Если DNS уже смотрит на сервер и порты 80/443 открыты, Caddy сам выпустит сертификат.
