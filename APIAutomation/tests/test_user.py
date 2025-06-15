import pytest
import allure
import time
import json
from base.base_test import BaseTest
from config.settings import URLs, Headers, TestData
from utils.data_generator import DataGenerator

@allure.epic("Pet Store API")
@allure.feature("User Management")
@allure.suite("User Suite")
class TestUser(BaseTest):
    def setup_method(self):
        """
        Her test metodundan önce çalışır ve test verilerini hazırlar
        """
        self.data_generator = DataGenerator()
        self.user_data = self.data_generator.generate_user_data()
        self.username = self.user_data["username"]
        self.password = self.user_data["password"]
        self.headers_payload = Headers.CONTENT_TYPE_JSON

    def retry_until_success(self, operation, max_retries=TestData.MAX_RETRIES):
        """
        Belirtilen testi başarılı olana kadar tekrarlar.

        """
        for attempt in range(max_retries):
            response = operation()
            if response.status_code == 200:
                return response
            if attempt == max_retries - 1:
                self.logger.error(f"Operation failed after {max_retries} attempts. Last response: {response.text}")
        return response

    def create_user(self):
        """
        Yeni kullanıcı oluşturur ve başarılı yanıtı doğrular
        """
        with allure.step("Kullanıcı oluşturma isteği gönder"):
            allure.attach(str(self.user_data), name="Request Body", attachment_type=allure.attachment_type.JSON)
            response = self.post(URLs.USER_ENDPOINT, self.user_data, self.headers_payload)
            allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
            self.assert_equals(str(response.status_code), "200")
            return response

    @allure.title("Kullanıcı Oluştur")
    @allure.description("Bu test, yeni bir kullanıcı oluşturur ve başarılı bir yanıt alır.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("create", "user", "api")
    @allure.link("https://petstore.swagger.io/", name="Swagger Docs")
    def test_create_user(self):
        self.create_user()

    @allure.title("Kullanıcı Bilgisi Getir")
    @allure.description("Bu test, belirli bir kullanıcının bilgilerini getirir ve doğrular.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("get", "user", "api")
    @allure.issue("PS-107", "GET İşlemi idempotent değil")
    @allure.link("https://petstore.swagger.io/", name="Swagger Docs")
    def test_get_user_info(self):
        self.create_user()
        
        with allure.step("Kullanıcı bilgisi için GET isteği gönder"):
            response = self.retry_until_success(
                lambda: self.get(f"{URLs.USER_ENDPOINT}/{self.username}")
            )
            allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
            self.assert_equals(str(response.status_code), "200")
            self.assert_equals(response.json()["username"], self.username)
            self.assert_equals(response.json()["email"], self.user_data["email"])

    @allure.title("Kullanıcı Bilgilerini Güncelle")
    @allure.description("Bu test, kullanıcı bilgilerini günceller ve başarılı bir yanıt alır.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("update", "user", "api")
    @allure.link("https://petstore.swagger.io/", name="Swagger Docs")
    def test_update_user(self):
        # Önce kullanıcıyı oluştur
        self.create_user()
        
        updated_user_data = self.data_generator.generate_user_data()
        updated_user_data["username"] = self.username  # Kullanıcı adını koruyoruz
        
        with allure.step("Kullanıcı güncelleme isteği gönder"):
            allure.attach(str(updated_user_data), name="Request Body", attachment_type=allure.attachment_type.JSON)
            response = self.put(f"{URLs.USER_ENDPOINT}/{self.username}", updated_user_data, self.headers_payload)
            allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
            self.assert_equals(str(response.status_code), "200")

    @allure.title("Kullanıcı Sil")
    @allure.description("""
    Bu test, kullanıcıyı siler ve başarılı bir yanıt alır.
    
    Bilinen Bug:
    - DELETE işlemi idempotent değil
    - Aynı kullanıcı için birden fazla DELETE isteği gönderildiğinde 404 hatası alınıyor
    - REST API best practice'lerine göre DELETE işlemi idempotent olmalıdır
    - Bug ID: PS-107
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("delete", "user", "api")
    @allure.issue("PS-108", "DELETE işlemi idempotent değil")
    @allure.link("https://petstore.swagger.io/", name="Swagger Docs")
    def test_delete_user(self):
        self.create_user()
        
        with allure.step("Kullanıcı silme isteği gönder"):
            delete_url = f"{URLs.USER_ENDPOINT}/{self.username}"
            response = self.retry_until_success(
                lambda: self.delete(delete_url)
            )
            allure.attach(f"Delete Response Status: {response.status_code}",
                         name="Delete Response Status",
                         attachment_type=allure.attachment_type.TEXT)
            allure.attach(response.text,
                         name="Delete Response Body",
                         attachment_type=allure.attachment_type.JSON)
            self.assert_equals(str(response.status_code), "200")
            
            # Silinen kullanıcının artık erişilemez olduğunu doğrula
            verify_delete_response = self.get(f"{URLs.USER_ENDPOINT}/{self.username}")
            self.assert_equals(str(verify_delete_response.status_code), "404")

            # Bug PS-107: DELETE işlemi idempotent değil
            second_delete_response = self.delete(delete_url)
            if second_delete_response.status_code != 200:
                allure.attach("""
                Bug PS-107: DELETE işlemi idempotent değil
                - İkinci DELETE isteği 404 dönüyor
                - REST API best practice'lerine göre DELETE işlemi idempotent olmalıdır
                - Aynı kaynağa yapılan birden fazla DELETE isteği aynı sonucu vermelidir
                """, name="Bug Report", attachment_type=allure.attachment_type.TEXT)

    @allure.title("Kullanıcı Girişi")
    @allure.description("Bu test, kullanıcı girişi yapar ve başarılı bir yanıt alır.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("login", "user", "api")
    @allure.link("https://petstore.swagger.io/", name="Swagger Docs")
    def test_login(self):
        # Önce kullanıcıyı oluştur
        self.create_user()
        
        with allure.step("Kullanıcı girişi isteği gönder"):
            response = self.get(f"{URLs.USER_ENDPOINT}/login?username={self.username}&password={self.password}")
            allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
            self.assert_equals(str(response.status_code), "200")

    @allure.title("Kullanıcı Çıkışı")
    @allure.description("Bu test, kullanıcı çıkışı yapar ve başarılı bir yanıt alır.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("logout", "user", "api")
    @allure.link("https://petstore.swagger.io/", name="Swagger Docs")
    def test_logout(self):
        with allure.step("Kullanıcı çıkışı isteği gönder"):
            response = self.get(f"{URLs.USER_ENDPOINT}/logout")
            allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
            self.assert_equals(str(response.status_code), "200")