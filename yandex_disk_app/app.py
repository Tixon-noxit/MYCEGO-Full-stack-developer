from flask import Flask, render_template, request, redirect, url_for, send_file
import requests
import os

app = Flask(__name__)
YANDEX_API_BASE_URL = "https://cloud-api.yandex.net/v1/disk/public/resources"



def get_files_list(public_key: str) -> list:
    """Подучает список файлов по публичной ссылке."""
    params = {'public_key': public_key}
    response = requests.get(YANDEX_API_BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('_embedded', {}).get('items', [])
        return items
    else:
        return []


@app.route('/', methods=['GET', 'POST'])
def index():
    """Маршрут для отображения списка файлов"""
    files = []
    if request.method == 'POST':
        public_key = request.form.get('public_key')
        files = get_files_list(public_key)
    return render_template('index.html', files=files)


def download_file(public_key: str, file_path: str) -> str:
    """Скачивает файл по публичной ссылке."""
    params = {'public_key': public_key, 'path': file_path}
    response = requests.get(YANDEX_API_BASE_URL + '/download', params=params)
    
    if response.status_code == 200:
        download_url = response.json().get('href')
        local_filename = file_path.split('/')[-1]
        file_data = requests.get(download_url)
        with open(local_filename, 'wb') as f:
            f.write(file_data.content)
        return local_filename
    else:
        return None

@app.route('/download', methods=['POST'])
def download():
    public_key = request.form.get('public_key')
    file_path = request.form.get('file_path')
    file_name = download_file(public_key, file_path)
    if file_name:
        return send_file(file_name, as_attachment=True)
    return "Ошибка при скачивании файла", 400


if __name__ == "__main__":
    app.run(debug = True)