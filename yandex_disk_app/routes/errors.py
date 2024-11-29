from flask import Blueprint, render_template

errors_bp = Blueprint('errors', __name__)


@errors_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Страница не найдена."), 404


@errors_bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_code=500, error_message="Внутренняя ошибка сервера."), 500


@errors_bp.app_errorhandler(403)
def forbidden(e):
    return render_template('error.html', error_code=403, error_message="Доступ запрещён."), 403


@errors_bp.app_errorhandler(400)
def bad_request(e):
    return render_template('error.html', error_code=400, error_message="Неверный запрос."), 400
