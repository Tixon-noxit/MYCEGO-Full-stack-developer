from flask import Flask, redirect, request, session, url_for, jsonify, render_template
import requests
import os

app = Flask(__name__)
YANDEX_API_BASE_URL = "https://cloud-api.yandex.net/v1/disk/public/resources"
HARDCODED_PUBLIC_KEY = "https://disk.yandex.ru/d/5YnoblFI4ZtKEA"

app.secret_key = 'your_secret_key'  # Для хранения сессий

# Конфигурация OAuth
CLIENT_ID = '31f68e50e9a542499c07ddb01ac8d073'
CLIENT_SECRET = '8407a81d5db3416d9a45c6313e68c498'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
YANDEX_AUTH_URL = 'https://oauth.yandex.ru/authorize'
YANDEX_TOKEN_URL = 'https://oauth.yandex.ru/token'


# Главная страница
@app.route('/')
def index():
    access_token = session.get('access_token')
    if access_token:
        return redirect(url_for('show_files'))
    else:
        context = {
            'authorized': False,
            'access_token': False,
        }
        return render_template('index.html', context=context)


# Авторизация
@app.route('/login')
def login():
    auth_url = f"{YANDEX_AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    return redirect(auth_url)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'Ошибка: код авторизации не получен.', 400

    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
    }

    response = requests.post(YANDEX_TOKEN_URL, data=token_data)
    if response.status_code != 200:
        return f"Ошибка получения токена: {response.text}", 400

    token = response.json()
    session['access_token'] = token['access_token']
    return redirect(url_for('show_files'))


# Просмотр файлов по публичной ссылке
@app.route('/show_files')
def show_files():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))

    headers = {'Authorization': f'OAuth {access_token}'}
    params = {'public_key': HARDCODED_PUBLIC_KEY}

    response = requests.get(f"{YANDEX_API_BASE_URL}", headers=headers, params=params)

    if response.status_code == 200:
        files = response.json()['_embedded']['items']
        context = {
            'files': files,
            'access_token': True,
        }
        return render_template('files.html', context=context)
    else:
        return f"Ошибка получения файлов: {response.text}", 400


@app.route('/browse')
def browse_folder():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))

    # Получение пути папки из параметра запроса
    path = request.args.get('path', '/')
    headers = {'Authorization': f'OAuth {access_token}'}

    # Запрос содержимого папки
    response = requests.get(
        'https://cloud-api.yandex.net/v1/disk/public/resources',
        params={'public_key': 'ваш_публичный_ключ', 'path': path},
        headers=headers
    )
    if response.status_code != 200:
        return f"Ошибка доступа: {response.text}", 400

    folder_content = response.json()
    files = [
        {
            'name': item['name'],
            'size': item.get('size'),
            'file': item.get('file'),
            'path': item['path']
        }
        for item in folder_content['_embedded']['items']
    ]
    return render_template('files.html', context={'files': files})


@app.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        'error.html',
        error_code=404,
        error_message="К сожалению, запрашиваемая страница не найдена."
    ), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template(
        'error.html',
        error_code=500,
        error_message="Что-то пошло не так. Пожалуйста, попробуйте позже."
    ), 500


@app.errorhandler(403)
def forbidden(e):
    return render_template(
        'error.html',
        error_code=403,
        error_message="Доступ запрещён. У вас нет прав для просмотра этой страницы."
    ), 403


@app.errorhandler(400)
def forbidden(e):
    return render_template(
        'error.html',
        error_code=400,
        error_message="Не удалось найти запрошенный ресурс."
    ), 400


if __name__ == "__main__":
    app.run(debug=True)
