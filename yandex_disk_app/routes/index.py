"""
Маршруты для основного модуля (index).

Этот модуль обрабатывает отображение главной страницы и перенаправление
на страницу авторизации Яндекса через OAuth.
"""

from flask import Blueprint, session, redirect, url_for, render_template, flash
from config import YANDEX_AUTH_URL, CLIENT_ID, REDIRECT_URI
from oauth import get_access_token

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index() -> str:
    """
    Отображение главной страницы приложения.

    Возвращает:
        str: HTML-код главной страницы.
    """
    return render_template('index.html')


@index_bp.route('/login')
def login() -> 'werkzeug.wrappers.Response':
    """
    Перенаправление пользователя на страницу авторизации Яндекса.

    Формирует URL для авторизации через OAuth с необходимыми параметрами
    и выполняет редирект.

    Возвращает:
        werkzeug.wrappers.Response: Ответ с редиректом на страницу авторизации Яндекса.
    """
    auth_url = f"{YANDEX_AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    return redirect(auth_url)


@index_bp.route('/callback')
def callback() -> 'werkzeug.wrappers.Response':
    """
    Обработка кода авторизации от Яндекса и получение токена доступа.

    Если код авторизации отсутствует, перенаправляет на главную страницу.
    При успешном получении токена проверяет наличие `public_key` в сессии
    и, если он указан, перенаправляет пользователя в папку.
    В противном случае возвращает на главную страницу.

    Возвращает:
        werkzeug.wrappers.Response: Ответ с редиректом на соответствующую страницу.
    """
    from flask import request, session

    code = request.args.get('code')
    if not code:
        flash("Ошибка: код авторизации не получен.")
        return redirect(url_for('index.index'))

    token, error = get_access_token(code)
    if error:
        flash(f"Ошибка получения токена: {error}")
        return redirect(url_for('index.index'))

    public_key = session.get('public_key')
    if public_key:
        return redirect(url_for('files.browse_folder', public_key=public_key))

    return redirect(url_for('index.index'))


@index_bp.route('/logout')
def logout() -> 'werkzeug.wrappers.Response':
    """
    Выход из системы и удаление токена из сессии.

    Удаляет `access_token` и `public_key` из текущей сессии и перенаправляет пользователя
    на главную страницу.

    Возвращает:
        werkzeug.wrappers.Response: Ответ с редиректом на главную страницу.
    """
    session.pop('access_token', None)
    session.pop('public_key', None)
    return redirect(url_for('index.index'))
