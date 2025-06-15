import os
import sys
import pytest
import subprocess
import webbrowser
import shutil

# Proje kök dizinini Python path'ine ekle
# Proje kök dizininin mutlak yolunu al
project_root = os.path.dirname(os.path.abspath(__file__))

# Proje kök dizinini Python path'ine ekle
sys.path.insert(0, project_root)

# Özel işaretleyicileri kaydet
def pytest_configure(config):
    config.addinivalue_line("markers", "order: mark test to run in a specific order")

# @pytest.fixture(scope="session", autouse=True)
# def setup_teardown(request):
#     """
#     Test oturumu başlamadan önce ve bittikten sonra çalışacak fixture.
#     CI/CD ortamında otomatik rapor oluşturur.
#     """
#     # Only clean and create the allure-results directory on the master process
#     if not hasattr(request.config, 'workerinput'):
#         print("\n--- Cleaning allure-results directory on master process ---")
#         if os.path.exists("./allure-results"):
#             shutil.rmtree("./allure-results")
#         os.makedirs("./allure-results", exist_ok=True)

    yield

    # After - Sadece CI/CD ortamında rapor oluştur (Sadece master process üzerinde çalışır)
    if not hasattr(request.config, 'workerinput'):
        if os.getenv("CI"):
            if os.path.exists("./allure-report"):
                shutil.rmtree("./allure-report")
            subprocess.run("allure generate ./allure-results --clean", shell=True) 