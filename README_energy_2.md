# energy_2 — сайт продажи энергетиков

Production-деплой этого проекта сделан по схеме:

**GitHub Actions → Docker Hub → Yandex Cloud VM → Caddy → домен `sharashkinakontora.shop`**

Это значит:

- при `git push` в `main` GitHub Actions собирает Docker image;
- image пушится в Docker Hub;
- на сервер по SSH отправляются только `docker-compose.prod.yml`, `Caddyfile` и production `.env`;
- на сервере выполняется `docker compose pull` и `docker compose up -d`;
- сайт работает через домен:
  - `sharashkinakontora.shop`
  - `www.sharashkinakontora.shop`

Такая схема удобна тем, что при смене **динамического IP** тебе обычно достаточно поменять **A-записи в REG.RU**, и сайт снова будет открываться по домену.

---

## 1. Что нужно один раз подготовить

### На сервере (Yandex Cloud VM)

На сервере должны быть установлены:

- Docker Engine
- Docker Compose plugin
- SSH-доступ

Проверка:

```bash
docker --version
docker compose version
```

Если на сервере ещё не создана папка деплоя:

```bash
mkdir -p /home/energy/energy_2
```

Если GitHub Actions будет подключаться по отдельному deploy-ключу, его **публичная часть** должна быть добавлена в:

```bash
~/.ssh/authorized_keys
```

---

## 2. Что нужно в Docker Hub

Создай репозиторий:

```text
energy_2
```

Лучше сделать его **Public**, чтобы сервер мог тянуть образ без отдельного `docker login`.

Также создай **Docker Hub Access Token** — он нужен для GitHub Actions.

---

## 3. Что нужно в GitHub Secrets

Открой:

```text
Repository → Settings → Secrets and variables → Actions
```

И добавь следующие secrets.

### `DOCKERHUB_USERNAME`
Твой логин в Docker Hub.

Пример:

```text
mydockername
```

### `DOCKERHUB_TOKEN`
Твой Docker Hub Access Token.

### `SSH_HOST`
Для этого проекта лучше использовать **домен**, а не IP:

```text
sharashkinakontora.shop
```

### `SSH_PORT`
Обычно:

```text
22
```

### `SSH_USER`
У тебя сейчас:

```text
energy
```

### `DEPLOY_PATH`
Путь на сервере:

```text
/home/energy/energy_2
```

### `SSH_PRIVATE_KEY`
Приватный deploy-ключ, которым GitHub Actions будет входить на сервер.

Вставлять нужно **полное содержимое файла**, например:

```text
-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----
```

### `SSH_KNOWN_HOSTS`
Host key сервера **по домену**.

Получить на Windows PowerShell:

```powershell
ssh-keyscan -H -t ed25519 sharashkinakontora.shop
```

В secret вставляется **одна нормальная строка known_hosts**, а не ошибки.

### `DJANGO_ENV_FILE`
Полный production `.env`, который будет загружаться на сервер как файл `.env`.

Готовый пример:

```env
SECRET_KEY=django-insecure-change-me-very-long-production-key
DEBUG=0
ALLOWED_HOSTS=sharashkinakontora.shop,www.sharashkinakontora.shop
CSRF_TRUSTED_ORIGINS=https://sharashkinakontora.shop,https://www.sharashkinakontora.shop
POSTGRES_DB=start_energy
POSTGRES_USER=start_user
POSTGRES_PASSWORD=replace-with-strong-password
POSTGRES_HOST=db
POSTGRES_PORT=5432
FORCE_HTTPS=1
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@sharashkinakontora.shop
DJANGO_SUPERUSER_PASSWORD=replace-with-strong-admin-password
DOCKERHUB_USERNAME=your_dockerhub_username
```

Важно: строка `DOCKERHUB_USERNAME` в `DJANGO_ENV_FILE` должна совпадать с твоим реальным Docker Hub username.

---

## 4. Что должно быть у домена в REG.RU

В DNS должны быть записи:

- `A` для `@` → текущий публичный IP ВМ
- `A` для `www` → текущий публичный IP ВМ

Если IP ВМ изменился:

1. узнаёшь новый IP;
2. меняешь `A` запись `@`;
3. меняешь `A` запись `www`;
4. ждёшь обновление DNS.

После этого сайт снова откроется по домену.

---

## 5. Что должно быть открыто на сервере

Для работы сайта и HTTPS должны быть доступны:

- `22/tcp` — SSH
- `80/tcp` — HTTP
- `443/tcp` — HTTPS

Если используется firewall / security group — проверь эти правила.

---

## 6. Как работает деплой

Workflow запускается при:

- `push` в `main`
- `push` в `master`
- ручном запуске через GitHub Actions

Что он делает:

1. делает checkout проекта;
2. логинится в Docker Hub;
3. собирает image;
4. пушит его в Docker Hub;
5. по SSH создаёт папку деплоя на сервере;
6. отправляет на сервер:
   - `docker-compose.prod.yml`
   - `Caddyfile`
   - `.env`
7. на сервере выполняет:

```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

---

## 7. Как сделать первый деплой

После того как заполнены все GitHub Secrets:

1. сделай любой новый commit;
2. отправь его в `main`;
3. открой вкладку **Actions** в GitHub;
4. открой workflow деплоя;
5. смотри, на каком шаге всё прошло или упало.

Пример:

```bash
git add .
git commit -m "Deploy setup"
git push origin main
```

---

## 8. Как проверить сервер после деплоя

Подключись к серверу:

```bash
ssh -i C:\Users\PC\.ssh\id_ed25519_energy energy@sharashkinakontora.shop
```

Потом:

```bash
cd /home/energy/energy_2
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs --tail=100
```

---

## 9. Если IP меняется

Если это **та же самая ВМ**, и у неё просто сменился публичный IP после stop/start:

- обычно достаточно поменять A-записи в REG.RU;
- GitHub Actions тоже продолжит ходить по домену, если домен уже указывает на новый IP;
- `SSH_KNOWN_HOSTS` обычно менять не нужно, если это та же самая ВМ и её SSH host key не менялся.

Если это **совсем новая ВМ**, тогда дополнительно нужно:

- снова установить Docker;
- снова добавить deploy-ключ в `authorized_keys`;
- при необходимости обновить `SSH_KNOWN_HOSTS`.

---

## 10. Полезная логика для тебя

Твоя удобная схема теперь такая:

- проект хранится в GitHub;
- Docker image хранится в Docker Hub;
- домен живёт в REG.RU;
- сервер в Yandex Cloud можно выключать;
- если IP поменялся — ты меняешь только DNS в REG.RU;
- после этого сайт снова доступен по домену.

