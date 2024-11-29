from flask import Blueprint, session, redirect, url_for, render_template, g, flash
from config import YANDEX_AUTH_URL, CLIENT_ID, REDIRECT_URI
from oauth import get_access_token

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')


@index_bp.route('/login')
def login():
    """Редирект на страницу авторизации Яндекса"""
    auth_url = f"{YANDEX_AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    return redirect(auth_url)


@index_bp.route('/callback')
def callback():
    """Обработка кода авторизации и получение токена"""
    from flask import request, session

    code = request.args.get('code')
    if not code:
        return 'Ошибка: код авторизации не получен.', 400

    token, error = get_access_token(code)
    if error:
        return f"Ошибка получения токена: {error}", 400

    public_key = session.get('public_key')
    if public_key:
        return redirect(url_for('files.browse_folder', public_key=public_key))

    return redirect(url_for('index.index'))


@index_bp.route('/logout')
def logout():
    """Выход из системы"""
    session.pop('access_token', None)
    return redirect(url_for('index.index'))
