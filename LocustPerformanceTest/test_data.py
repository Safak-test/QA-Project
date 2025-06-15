import random
from config import Config

class TestDataGenerator:
    @staticmethod
    def generate_pet_data(pet_id=None):
        """Generate random pet data for testing"""
        if pet_id is None:
            pet_id = random.randint(1, 1000)
            
        return {
            "id": pet_id,
            "category": {
                "id": random.randint(1, 5),
                "name": random.choice(Config.PET_CATEGORIES)
            },
            "name": random.choice(Config.PET_NAMES),
            "photoUrls": [
                f"https://example.com/pet_{pet_id}.jpg"
            ],
            "tags": [
                {
                    "id": random.randint(1, 10),
                    "name": f"tag_{random.randint(1, 5)}"
                }
            ],
            "status": random.choice(Config.PET_STATUSES)
        }
    
    @staticmethod
    def generate_pet_id():
        """Generate a random pet ID"""
        return random.randint(1, 1000) 