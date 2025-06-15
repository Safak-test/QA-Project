class Config:
    # Base URL for the Pet Store API
    BASE_URL = "https://petstore.swagger.io/v2"
    
    # Test Configuration
    MIN_WAIT_TIME = 1
    MAX_WAIT_TIME = 3
    
    # Test Data
    PET_CATEGORIES = ["dogs", "cats", "birds", "fish"]
    PET_NAMES = ["Buddy", "Max", "Bella", "Charlie", "Luna", "Lucy", "Cooper", "Daisy"]
    PET_STATUSES = ["available", "pending", "sold"]
    
    # Headers
    HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Test Scenarios
    SCENARIO_WEIGHTS = {
        "add_pet": 2,
        "get_pet": 3,
        "update_pet": 1,
        "delete_pet": 1
    } 