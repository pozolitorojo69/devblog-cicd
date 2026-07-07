# ================================
# SELENIUM E2E FIXTURES
# ================================

import threading
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from app import create_app
from app.models import blog_storage


# Fixture requerido por pytest-flask
@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    return app


# Reinicia el almacenamiento antes de cada prueba
@pytest.fixture(autouse=True)
def reset_blog_storage():
    blog_storage._posts.clear()
    blog_storage._next_id = 1
    blog_storage._create_sample_posts()


# Inicia Flask para las pruebas E2E
@pytest.fixture(scope="session")
def flask_test_app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    def run_app():
        app.run(
            host="127.0.0.1",
            port=5001,
            debug=False,
            use_reloader=False,
        )

    server_thread = threading.Thread(target=run_app, daemon=True)
    server_thread.start()
    time.sleep(3)

    yield app


# Driver de Selenium
@pytest.fixture
def selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


# URL base para las pruebas E2E
@pytest.fixture
def e2e_base_url():
    return "http://127.0.0.1:5001"