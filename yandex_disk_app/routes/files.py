from flask import Blueprint, request, render_template, redirect
from oauth import ensure_token
import requests
from config import YANDEX_API_BASE_URL, HARDCODED_PUBLIC_KEY

files_bp = Blueprint('files', __name__)


@files_bp.route('/show_files')
def show_files():
    """Отображение файлов"""
    access_token = ensure_token()
    if isinstance(access_token, str) is False:
        return access_token

    headers = {'Authorization': f'OAuth {access_token}'}
    params = {'public_key': HARDCODED_PUBLIC_KEY}

    response = requests.get(f"{YANDEX_API_BASE_URL}", headers=headers, params=params)
    if response.status_code == 200:
        files = response.json()['_embedded']['items']
        return render_template('files.html', context={'files': files})
    return f"Ошибка получения файлов: {response.text}", 400


@files_bp.route('/browse', endpoint='browse_folder')
def browse_folder():
    """Просмотр содержимого папки"""
    access_token = ensure_token()
    if isinstance(access_token, str) is False:
        return access_token

    path = request.args.get('path', '/')
    headers = {'Authorization': f'OAuth {access_token}'}
    params = {'public_key': HARDCODED_PUBLIC_KEY, 'path': path}

    response = requests.get(f"{YANDEX_API_BASE_URL}", headers=headers, params=params)
    if response.status_code == 200:
        folder_content = response.json()
        files = folder_content['_embedded']['items']

        breadcrumbs = []
        if path != '/':
            parts = path.strip('/').split('/')
            for i, part in enumerate(parts):
                breadcrumbs.append({
                    'name': part,
                    'path': '/' + '/'.join(parts[:i + 1])
                })

        return render_template(
            'files.html',
            context={'files': files, 'breadcrumbs': breadcrumbs, 'current_path': path}
        )
    return f"Ошибка доступа: {response.text}", 400
