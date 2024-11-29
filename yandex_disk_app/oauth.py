import requests
from flask import session, redirect, url_for
from config import YANDEX_TOKEN_URL, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


def get_access_token(code):
    """Получение access_token по коду авторизации"""
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
    }
    response = requests.post(YANDEX_TOKEN_URL, data=token_data)
    if response.status_code != 200:
        return None, response.text
    token = response.json()
    session['access_token'] = token['access_token']
    return token['access_token'], None


def ensure_token():
    """Проверяет наличие токена в сессии"""
    if 'access_token' not in session:
        return redirect(url_for('index'))
    return session.get('access_token')
