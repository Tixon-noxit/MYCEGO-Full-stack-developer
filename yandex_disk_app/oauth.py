"""
Модуль реализует функции для работы с OAuth-авторизацией через API Яндекс.Диск.

Основное назначение модуля — получение и проверка access_token,
который используется для доступа к публичным ресурсам Яндекс.Диска.
"""

from typing import Any

import requests
from flask import session, redirect, url_for, flash, Response
from config import YANDEX_TOKEN_URL, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from routes.files import parse_message_in_error


def get_access_token(code) -> Response | tuple[Any, None]:
    """
    Получение `access_token` по коду авторизации.

    Args:
        code (str): Код авторизации, предоставленный OAuth.

    Returns:
        tuple: Кортеж из двух элементов:
            - `str | None`: Полученный access_token, если запрос успешен.
            - `str | None`: Сообщение об ошибке, если запрос неуспешен.
    """
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
    }
    response = requests.post(YANDEX_TOKEN_URL, data=token_data)
    if response.status_code != 200:
        flash(f"Ошибка получения токена: {parse_message_in_error(response.text)}")
        return redirect(url_for('index.index'))
    token = response.json()
    session['access_token'] = token['access_token']
    return token['access_token'], None


def ensure_token() -> Response | None | Any:
    """
    Проверка наличия `access_token` в сессии.

    Returns:
        str | None: `access_token`, если он существует в сессии, иначе перенаправление на главную страницу.
    """
    if 'access_token' not in session:
        return redirect(url_for('index'))
    return session.get('access_token')
