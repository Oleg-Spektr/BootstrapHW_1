import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# Вычисляем абсолютный путь к файлу шаблона contacts.html (находится в корне проекта)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_FILE_PATH = os.path.join(BASE_DIR, "contacts.html")


class MyWebServer(BaseHTTPRequestHandler):

    # КРИТЕРИЙ 4, 5, 6: Обработка GET-запросов и чтение файла через контекстный менеджер
    def do_GET(self):
        # Сервер обрабатывает /, /contacts и /index.html
        if self.path in ['/', '/contacts', '/index.html']:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            # Чтение файла происходит строго по абсолютному пути HTML_FILE_PATH
            try:
                with open(HTML_FILE_PATH, "r", encoding="utf-8") as file:
                    html_content = file.read()
                self.wfile.write(bytes(html_content, "utf-8"))
            except FileNotFoundError:
                self.wfile.write(bytes("<h3>Ошибка: Файл contacts.html не найден в корне проекта!</h3>", "utf-8"))

        # Дополнительный функционал: Возврат кастомной страницы 404 ошибки
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            error_html = """
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <link href="https://jsdelivr.net" rel="stylesheet">
                <title>404 - Страница не найдена</title>
            </head>
            <body class="d-flex align-items-center justify-content-center vh-100 bg-light">
                <div class="text-center card p-5 shadow-sm">
                    <h1 class="display-1 fw-bold text-danger">404</h1>
                    <p class="fs-3"> <span class="text-danger">Ой!</span> Страница не найдена.</p>
                    <p class="lead">Запрашиваемый вами адрес не существует.</p>
                    <a href="/" class="btn btn-primary">Вернуться на Главную</a>
                </div>
            </body>
            </html>
            """
            self.wfile.write(bytes(error_html, "utf-8"))

    # КРИТЕРИЙ 7: Прием POST-запроса с формы и вывод данных в консоль без ошибок
    def do_POST(self):
        # Обрабатываем отправку формы как на корень, так и на /contacts
        if self.path in ['/', '/contacts']:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Разбираем url-encoded данные формы в удобный словарь
            parsed_data = urllib.parse.parse_qs(post_data)

            print("\n=== ПОЛУЧЕНЫ ДАННЫЕ ИЗ HTML-ФОРМЫ ===")
            for key, value in parsed_data.items():
                # Извлекаем чистое значение из списка
                clean_value = value[0] if value else ''
                print(f"{key}: {clean_value}")
            print("========================================\n")

            # Отдаем пользователю корректный HTML-ответ об успешной отправке
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            success_html = """
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <link href="https://jsdelivr.net" rel="stylesheet">
                <title>Успешно отправлено</title>
            </head>
            <body class="d-flex align-items-center justify-content-center vh-100 bg-light">
                <div class="text-center card p-4 shadow-sm" style="max-width: 500px;">
                    <h3 class="text-success mb-3">Данные успешно получены сервером!</h3>
                    <p class="text-muted">Сообщение обработано и выведено в консоль PyCharm.</p>
                    <a href="/contacts" class="btn btn-outline-primary">Назад к контактам</a>
                </div>
            </body>
            </html>
            """
            self.wfile.write(bytes(success_html, "utf-8"))


def run(server_class=HTTPServer, handler_class=MyWebServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен и стабильно работает на http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")


if __name__ == '__main__':
    run()
