from flask import Blueprint, request, render_template, g, redirect, url_for, flash
import requests, re
import json
from config import YANDEX_API_BASE_URL

files_bp = Blueprint('files', __name__)


def get_public_key(public_key_or_url):
    url_pattern = r"https?://disk\.yandex\.ru/(public/)?[a-z]/([A-Za-z0-9_-]+)"
    match = re.match(url_pattern, public_key_or_url)
    if match:
        return match.group(2)
    return public_key_or_url


def parse_message_in_error(response_text):
    data = json.loads(response_text)
    return data.get("message", "Сообщение отсутствует")


def fetch_files_or_folders(access_token, public_key, path='/'):
    headers = {'Authorization': f'OAuth {access_token}'}
    params = {'public_key': f'https://disk.yandex.ru/d/{public_key}', 'path': path, 'preview_size': 'M'}

    response = requests.get(f"{YANDEX_API_BASE_URL}", headers=headers, params=params)
    if response.status_code == 200:
        folder_content = response.json()
        files = folder_content['_embedded']['items']
        return files, None

    error_message = parse_message_in_error(response.text)
    return None, error_message


@files_bp.route('/show_files')
def show_files():
    """Отображение файлов"""
    from flask import session

    access_token = g.access_token
    if not access_token:
        return redirect(url_for('index.index'))

    public_key = get_public_key(request.args.get('public_key') or session.get('public_key'))
    if not public_key:
        flash("Путь к папке не указан")
        return redirect(url_for('index.index'))

    session['public_key'] = public_key

    files, error_message = fetch_files_or_folders(access_token, public_key)
    if error_message:
        flash(f"Ошибка: {error_message}")
        return redirect(url_for('index.index'))

    context = {'files': files}
    return render_template('files.html', context=context)


@files_bp.route('/browse', endpoint='browse_folder')
def browse_folder():
    """Просмотр содержимого папки"""
    from flask import session

    path = request.args.get('path', '/')
    public_key = get_public_key(request.args.get('public_key') or session.get('public_key'))
    if not public_key:
        flash("Путь к папке не указан")
        return redirect(url_for('index.index'))

    if 'public_key' not in session or session['public_key'] != public_key:
        session['public_key'] = public_key

    access_token = g.access_token
    if not access_token:
        return redirect(url_for('index.login'))

    files, error_message = fetch_files_or_folders(access_token, public_key, path)
    if error_message:
        flash(f"Ошибка: {error_message}")
        return redirect(url_for('index.index'))

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
