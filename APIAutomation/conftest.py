import os
import sys
import pytest
import subprocess
import webbrowser
import shutil

# Get the absolute path of the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Add the project root directory to Python path
sys.path.insert(0, project_root)

# Register custom marks
def pytest_configure(config):
    config.addinivalue_line("markers", "order: mark test to run in a specific order")

@pytest.fixture(scope="session", autouse=True)
def setup_teardown():
    """
    Test oturumu başlamadan önce ve bittikten sonra çalışacak fixture.
    CI/CD ortamında otomatik rapor oluşturur.
    """
    # Before - Test dizinini temizle
    if os.path.exists("./allure-results"):
        shutil.rmtree("./allure-results")
    os.makedirs("./allure-results")
    
    yield
    
    # After - Sadece CI/CD ortamında rapor oluştur
    if os.getenv("CI"):
        if os.path.exists("./allure-report"):
            shutil.rmtree("./allure-report")
        subprocess.run("allure generate ./allure-results --clean", shell=True) 