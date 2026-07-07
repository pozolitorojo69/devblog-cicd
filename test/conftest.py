# ================================
# SELENIUM E2E FIXTURES
# ================================
import threading
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from app import create_app


@pytest.fixture(scope="session")
def flask_test_app():
    """Fixture que inicia la aplicación Flask para testing E2E."""
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


@pytest.fixture
def selenium_driver():
    """Fixture que crea un driver de Chrome para testing."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    yield driver

    driver.quit()


@pytest.fixture
def e2e_base_url():
    """URL base para los tests E2E (nombre diferente para evitar conflictos)."""
    return "http://127.0.0.1:5001"