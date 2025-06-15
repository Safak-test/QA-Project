"""
Base Test Class for API Test Automation Framework
"""
import allure
import logging
from config.settings import URLs, Headers, TestData, Framework
from base.base_library import BaseLibrary

class BaseTest(BaseLibrary):
    """
    Base test class that all test classes should inherit from.
    Provides common functionality and configuration for all tests.
    """
    def setup_method(self):
        """
        Setup method that runs before each test method.
        Initializes common test attributes and configurations.
        """
        # Initialize logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(Framework.LOG_LEVEL)
        
        # Initialize common attributes
        self.base_url = URLs.BASE_URL
        self.headers = Headers.CONTENT_TYPE_JSON
        self.max_retries = TestData.MAX_RETRIES
        self.retry_delay = TestData.RETRY_DELAY

    def log_test_info(self, test_name, description=None):
        """
        Logs test information using Allure
        """
        allure.dynamic.title(test_name)
        if description:
            allure.dynamic.description(description)

    def log_request_details(self, method, url, payload=None, headers=None):
        """
        Logs request details using Allure
        """
        allure.attach(f"{method} Request URL: {url}",
                     name="Request URL",
                     attachment_type=allure.attachment_type.TEXT)
        if payload:
            allure.attach(str(payload),
                         name="Request Body",
                         attachment_type=allure.attachment_type.JSON)
        if headers:
            allure.attach(str(headers),
                         name="Request Headers",
                         attachment_type=allure.attachment_type.JSON)

    def log_response_details(self, response):
        """
        Logs response details using Allure
        """
        allure.attach(f"Response Status Code: {response.status_code}",
                     name="Response Status",
                     attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text,
                     name="Response Body",
                     attachment_type=allure.attachment_type.JSON) 