from flask import Flask
from config import SECRET_KEY
from routes.index import index_bp
from routes.files import files_bp
from routes.errors import errors_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Регистрация блюпринтов
app.register_blueprint(index_bp)
app.register_blueprint(files_bp)
app.register_blueprint(errors_bp)

if __name__ == "__main__":
    app.run(debug=True)
