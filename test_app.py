import pytest
from playwright.sync_api import sync_playwright

def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Запуск браузера в видимом режиме
        page = browser.new_page()
        page.goto("http://localhost:5000/login")

        # Вводим данные для авторизации
        page.fill('input[name="username"]', 'test_user')
        page.fill('input[name="password"]', 'test_password')
        page.click('button[type="submit"]')

        # Проверка успешного входа
        body_text = page.inner_text("body")
        assert "Welcome, test_user" in body_text

        browser.close()


def test_add_new_entry():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Авторизация
        page.goto("http://localhost:5000/login")
        page.fill('input[name="username"]', 'test_user')
        page.fill('input[name="password"]', 'test_password')
        page.click('button[type="submit"]')

        # Переход на страницу добавления новой записи
        page.goto("http://localhost:5000")

        # Заполнение формы добавления новой записи
        page.fill('input[name="description"]', 'Test Entry')
        page.click('button[type="submit"]')  # Нажимаем на кнопку отправки формы

        # Проверка добавления новой записи
        body_text = page.inner_text("body")
        assert "Test Entry" in body_text

        browser.close()


if __name__ == "__main__":
    pytest.main(["-v", "-s", "test_login.py"])
    pytest.main(["-v", "-s", "test_add_new_entry.py"])