"""
API Test Automation Framework Configuration Settings
"""

# API Base URLs
class URLs:
    BASE_URL = "https://petstore.swagger.io/v2"
    USER_ENDPOINT = f"{BASE_URL}/user"
    PET_ENDPOINT = f"{BASE_URL}/pet"
    STORE_ENDPOINT = f"{BASE_URL}/store"

# API Headers
class Headers:
    CONTENT_TYPE_JSON = {
        "Content-Type": "application/json"
    }

# Test Data Settings
class TestData:
    MAX_RETRIES = 20
    PASSWORD_LENGTH = 8

# Framework Settings
class Framework:
    LOG_LEVEL = "INFO"
    SCREENSHOT_DIR = "screenshots"
    REPORT_DIR = "reports"
    ALLURE_RESULTS_DIR = "allure-results" 