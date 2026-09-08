import unittest
import threading
import time
import urllib.request
import urllib.parse
import os
from http.server import HTTPServer
from src.server import MyWebServer, HTML_FILE_PATH


class TestWebServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_address = ('localhost', 8001)
        cls.httpd = HTTPServer(cls.server_address, MyWebServer)
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def test_get_home_page(self):
        url = "http://localhost:8001/"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.getcode(), 200)

    def test_get_404_page(self):
        url = "http://localhost:8001/some-random-page-123"
        with self.assertRaises(urllib.error.HTTPError) as cm:
            with urllib.request.urlopen(url):
                pass
        self.assertEqual(cm.exception.code, 404)

    # НОВЫЙ ТЕСТ: Проверка отправки формы через POST-запрос
    def test_post_contact_form(self):
        url = "http://localhost:8001/"
        data = urllib.parse.urlencode({
            'username': 'TestUser',
            'email': 'test@example.com',
            'message': 'Hello from test!'
        }).encode('utf-8')

        req = urllib.request.Request(url, data=data, method='POST')
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.getcode(), 200)
            body = response.read().decode('utf-8')
            self.assertIn("Данные успешно получены сервером!", body)

    # НОВЫЙ ТЕСТ: Имитация отсутствия HTML-файла
    def test_file_not_found_handling(self):
        # Временно переименуем рабочий файл, чтобы спровоцировать ошибку
        temp_path = HTML_FILE_PATH + ".bak"
        if os.path.exists(HTML_FILE_PATH):
            os.rename(HTML_FILE_PATH, temp_path)

        try:
            url = "http://localhost:8001/"
            with urllib.request.urlopen(url) as response:
                body = response.read().decode('utf-8')
                self.assertIn("Ошибка: Файл contacts.html не найден!", body)
        finally:
            # Обязательно возвращаем файл на место после теста
            if os.path.exists(temp_path):
                os.rename(temp_path, HTML_FILE_PATH)


if __name__ == '__main__':
    unittest.main()
