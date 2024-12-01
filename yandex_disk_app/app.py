from dotenv import load_dotenv
from flask import Flask, session, g
from config import SECRET_KEY
from routes.index import index_bp
from routes.files import files_bp
from routes.errors import errors_bp

app = Flask(__name__)
load_dotenv()
app.secret_key = SECRET_KEY


@app.before_request
def before_request():
    """Функция для добавления глобальной переменной в контекст каждого запроса"""
    g.access_token = session.get('access_token')


app.register_blueprint(index_bp)
app.register_blueprint(files_bp)
app.register_blueprint(errors_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5008)
