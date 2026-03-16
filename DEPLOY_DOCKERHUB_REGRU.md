# Деплой energy_2 через Docker Hub + домен sharashkinakontora.shop

Что меняется в этой версии:

- GitHub Actions больше не заливает весь проект на сервер через `rsync`.
- GitHub Actions собирает Docker image и пушит его в Docker Hub.
- На сервер отправляются только `docker-compose.prod.yml`, `Caddyfile` и production `.env`.
- Сервер делает `docker compose pull` и `docker compose up -d`.
- Для деплоя используется домен `sharashkinakontora.shop`, поэтому при смене IP тебе обычно достаточно поменять A-запись в REG.RU.

## Что заменить в проекте

Распакуй этот архив **в корень проекта `energy_2`** с заменой файлов.

Будут заменены:

- `.github/workflows/deploy.yml`
- `docker-compose.prod.yml`
- `.env.example`
- `GITHUB_SECRETS_TEMPLATE.txt`

## Что нужно один раз на сервере

На сервере должны быть установлены:

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg rsync
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

Потом перелогинься.

Создай папку деплоя:

```bash
mkdir -p /home/energy/energy_2
```

## Какие GitHub secrets нужны

Смотри готовый шаблон в `GITHUB_SECRETS_TEMPLATE.txt`.

Главная идея такая:

- `SSH_HOST=sharashkinakontora.shop`
- `DEPLOY_PATH=/home/energy/energy_2`
- `DJANGO_ENV_FILE` содержит production `.env`
- в `DJANGO_ENV_FILE` добавлен `DOCKERHUB_USERNAME`

## Как работать при смене IP

1. Узнал новый IP ВМ.
2. В REG.RU поменял A-запись `@` на новый IP.
3. В REG.RU поменял A-запись `www` на новый IP.
4. Подождал обновление DNS.
5. Сайт снова работает по домену.
6. GitHub Actions тоже продолжает ходить по домену, если SSH host key у той же ВМ не менялся.

## Важный момент

Если это **та же самая ВМ**, а меняется только публичный IP после stop/start, обычно достаточно DNS.

Если ты создаёшь **совсем новую ВМ**, то надо ещё:

- заново установить Docker
- добавить deploy-ключ GitHub Actions в `~/.ssh/authorized_keys`
- при необходимости обновить `SSH_KNOWN_HOSTS`

## Пример команды для host key по домену

В PowerShell:

```powershell
ssh-keyscan -H -t ed25519 sharashkinakontora.shop
```

В `SSH_KNOWN_HOSTS` вставляется одна нормальная строка known_hosts, а не ошибки.
