# Aiogram3-template

Aiogram 3 template
```bash
cp ./docker-compose.dev.yaml ./docker-compose.yaml
cp ./dist.env ./.env
docker compose up --build
```
Copy dist.env to .env and fill it with your data
### i18n
You have to regenerate type hints for i18n after changing locales
```bash
i18n -ftl ./app/locales/ru.ftl -stub i18n_stub.pyi
```
It is needed only for IDE type hints. Don't affect the code
```bash
when-changed -1v app/locales/ru.ftl -c i18n -ftl ./app/locales/ru.ftl -stub i18n_stub.pyi
```
Or you can use this command to regenerate type hints automatically
