import os

# Конфигурация приложения
CLIENT_ID = os.getenv('CLIENT_ID', 'template_client_id')
CLIENT_SECRET = os.getenv('CLIENT_SECRET', 'template_client_secret')
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://127.0.0.1:5008/callback')
YANDEX_API_BASE_URL = os.getenv('YANDEX_API_BASE_URL', 'https://cloud-api.yandex.net/v1/disk/public/resources')
YANDEX_AUTH_URL = os.getenv('YANDEX_AUTH_URL', 'https://oauth.yandex.ru/authorize')
YANDEX_TOKEN_URL = os.getenv('YANDEX_TOKEN_URL', 'https://oauth.yandex.ru/token')
SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')
