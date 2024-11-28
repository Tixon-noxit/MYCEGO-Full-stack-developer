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






if __name__ == "__main__":
    app.run(debug = True)