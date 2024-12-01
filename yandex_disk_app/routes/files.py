"""
Модуль обработки файлов и папок на Яндекс.Диске.

Этот модуль предоставляет функции для отображения файлов, просмотра содержимого папки,
и фильтрации файлов по типу (изображения, видео, документы, папки).
"""

import json
import re
from typing import Any

import requests
from config import YANDEX_API_BASE_URL
from flask import Blueprint, request, render_template, g, redirect, url_for, flash, Response

files_bp = Blueprint('files', __name__)


def get_public_key(public_key_or_url) -> str:
    """
        Получение публичного ключа из URL или строки.

        Если переданный параметр является URL, извлекает ключ из URL.
        Если передан только ключ, возвращает его.

        Аргументы:
            public_key_or_url (str): Публичный ключ или URL.

        Возвращает:
            str: Публичный ключ.
        """
    url_pattern = r"https?://disk\.yandex\.ru/(public/)?[a-z]/([A-Za-z0-9_-]+)"
    match = re.match(url_pattern, public_key_or_url)
    if match:
        return match.group(2)
    return public_key_or_url


def parse_message_in_error(response_text) -> str:
    """
        Извлечение сообщения об ошибке из текста ответа.

        Аргументы:
            response_text (str): Текст ответа от сервера.

        Возвращает:
            str: Сообщение об ошибке.
        """
    data = json.loads(response_text)
    return data.get("message", "Сообщение отсутствует")


def fetch_files_or_folders(access_token, public_key, path='/') -> tuple[Any, None] | tuple[None, str]:
    """
        Получение файлов и папок с Яндекс.Диска.

        Аргументы:
            access_token (str): Токен доступа.
            public_key (str): Публичный ключ папки.
            path (str): Путь к папке на Диске (по умолчанию '/').

        Возвращает:
            tuple: Список файлов или папок и сообщение об ошибке (если есть).
        """
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
def show_files() -> Response | str:
    """
    Отображение списка файлов.

    Выполняет проверку наличия токена доступа и публичного ключа,
    затем загружает файлы с Яндекс.Диска и отображает их.
    """
    from flask import session

    access_token = g.access_token
    if not access_token:
        return redirect(url_for('index.index'))

    public_key = get_public_key(request.args.get('public_key') or session.get('public_key'))
    if not public_key:
        flash("Путь к папке не указан!")
        return redirect(url_for('index.index'))

    session['public_key'] = public_key

    files, error_message = fetch_files_or_folders(access_token, public_key)
    if error_message:
        flash(f"Ошибка: {error_message}")
        return redirect(url_for('index.index'))

    context = {'files': files}
    return render_template('files.html', context=context)


@files_bp.route('/browse', endpoint='browse_folder')
def browse_folder() -> Response | str:
    """
    Просмотр содержимого папки на Яндекс.Диске.

    Отображает файлы в папке с возможностью фильтрации по типам файлов
    (изображения, видео, документы, папки).
    """
    from flask import session

    path = request.args.get('path', '/')
    filter_type = request.args.get('type')
    public_key = get_public_key(request.args.get('public_key') or session.get('public_key'))
    if not public_key:
        flash("Путь к папке не указан!")
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

    if filter_type:
        files = [
            file for file in files
            if (
                       filter_type == 'image' and file.get('mime_type', '').startswith('image/')
               ) or (
                       filter_type == 'video' and file.get('mime_type', '').startswith('video/')
               ) or (
                       filter_type == 'document' and 'application/' in file.get('mime_type', '')
               ) or (
                       filter_type == 'folder' and file.get('type') == 'dir'
               )
        ]

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
        context={'files': files, 'breadcrumbs': breadcrumbs, 'current_path': path, 'filter_type': filter_type}
    )
