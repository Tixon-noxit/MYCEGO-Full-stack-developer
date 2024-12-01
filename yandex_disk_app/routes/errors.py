"""
Обработчики ошибок для приложения.

Этот модуль определяет страницы для отображения сообщений об ошибках
с соответствующими кодами HTTP-статусов.
"""

from flask import Blueprint, render_template

errors_bp = Blueprint('errors', __name__)


@errors_bp.app_errorhandler(404)
def page_not_found(e) -> tuple[str, int]:
    """
        Обработчик ошибки 404 (Страница не найдена).

        Возвращает страницу ошибки с описанием проблемы и кодом 404.

        Аргументы:
            e (Exception): Исключение, вызвавшее ошибку.

        Возвращает:
            tuple: Шаблон страницы ошибки и код 404.
        """
    return render_template('error.html', error_code=404, error_message="Страница не найдена."), 404


@errors_bp.app_errorhandler(500)
def internal_server_error(e) -> tuple[str, int]:
    """
        Обработчик ошибки 500 (Внутренняя ошибка сервера).

        Возвращает страницу ошибки с описанием проблемы и кодом 500.

        Аргументы:
            e (Exception): Исключение, вызвавшее ошибку.

        Возвращает:
            tuple: Шаблон страницы ошибки и код 500.
        """
    return render_template('error.html', error_code=500, error_message="Внутренняя ошибка сервера."), 500


@errors_bp.app_errorhandler(403)
def forbidden(e) -> tuple[str, int]:
    """
        Обработчик ошибки 403 (Доступ запрещён).

        Возвращает страницу ошибки с описанием проблемы и кодом 403.

        Аргументы:
            e (Exception): Исключение, вызвавшее ошибку.

        Возвращает:
            tuple: Шаблон страницы ошибки и код 403.
        """
    return render_template('error.html', error_code=403, error_message="Доступ запрещён."), 403


@errors_bp.app_errorhandler(400)
def bad_request(e) -> tuple[str, int]:
    """
        Обработчик ошибки 400 (Неверный запрос).

        Возвращает страницу ошибки с описанием проблемы и кодом 400.

        Аргументы:
            e (Exception): Исключение, вызвавшее ошибку.

        Возвращает:
            tuple: Шаблон страницы ошибки и код 400.
        """
    return render_template('error.html', error_code=400, error_message="Неверный запрос."), 400
