import os

# Конфигурация приложения
CLIENT_ID = '31f68e50e9a542499c07ddb01ac8d073'
CLIENT_SECRET = '8407a81d5db3416d9a45c6313e68c498'
REDIRECT_URI = 'http://127.0.0.1:5008/callback'
YANDEX_API_BASE_URL = "https://cloud-api.yandex.net/v1/disk/public/resources"
YANDEX_AUTH_URL = 'https://oauth.yandex.ru/authorize'
YANDEX_TOKEN_URL = 'https://oauth.yandex.ru/token'
SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
