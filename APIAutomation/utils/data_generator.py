from faker import Faker
import random

class DataGenerator:
    def __init__(self):
        self.fake = Faker('tr_TR')  # Türkçe veri üretimi için

    def generate_user_data(self):
        """
        Rastgele user data  üretir
        """
        username = f"{self.fake.user_name()}{random.randint(1, 9999)}"
        return {
            "id": 0,
            "username": username,
            "firstName": self.fake.first_name(),
            "lastName": self.fake.last_name(),
            "email": self.fake.email(),
            "password": self.fake.password(length=8),
            "phone": self.fake.phone_number(),
            "userStatus": 0
        }

    def get_username(self):
        """
        Rastgele kullanıcı adı üretir
        """
        return f"{self.fake.user_name()}{random.randint(1, 9999)}"

    def get_password(self):
        """
        Rastgele şifre üretir
        """
        return self.fake.password(length=8) 