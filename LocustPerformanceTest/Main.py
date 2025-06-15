from locust import HttpUser, between, task, events
import json
import logging
from config import Config
from test_data import TestDataGenerator
import random

# Sadece bu modül için loglama yapılandırması
logger = logging.getLogger(__name__)
# Bu logger'ın seviyesini INFO olarak ayarla.
logger.setLevel(logging.INFO)

# Eğer bu logger için henüz bir konsol handler yoksa oluştur
# Bu kontrol, modüllerin birden çok kez yüklenebileceği Locust'un yeniden yükleyicisinde önemlidir
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s: %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class PetStoreUser(HttpUser):
    wait_time = between(Config.MIN_WAIT_TIME, Config.MAX_WAIT_TIME)
    host = Config.BASE_URL
    
    def on_start(self):
        """Kullanıcı başladığında test verilerini başlat"""
        self.pet_ids = set()
        # Başlangıçta bir pet oluştur
        self._create_initial_pet()

    def _create_initial_pet(self):
        """Başlangıçta bir pet oluştur"""
        try:
            pet_data = TestDataGenerator.generate_pet_data()
            with self.client.post(
                "/pet",
                json=pet_data,
                headers=Config.HEADERS,
                catch_response=True
            ) as response:
                if response.status_code == 200:
                    self.pet_ids.add(pet_data["id"])
                    try:
                        response_json = response.json()
                        assert response_json["id"] == pet_data["id"], f"Eklenen pet ID'si beklenenden farklı: {response_json['id']}"
                        assert response_json["name"] == pet_data["name"], f"Eklenen pet adı beklenenden farklı: {response_json['name']}"
                        assert response_json["status"] == pet_data["status"], f"Eklenen pet durumu beklenenden farklı: {response_json['status']}"
                        pass 
                    except (json.JSONDecodeError, AssertionError) as e:
                        response.failure(f"Eklenen pet yanıtı doğrulanamadı: {e}")
                        logger.error(f"Eklenen pet yanıtı doğrulanamadı: {e}")
                else:
                    logger.error(f"Başlangıç peti oluşturulamadı (Durum Kodu: {response.status_code}): {response.text}")
        except Exception as e:
            logger.error(f"Başlangıç peti oluşturulurken hata: {str(e)}")

    @task(Config.SCENARIO_WEIGHTS["add_pet"])
    def add_pet(self):
        """Yeni bir pet ekle"""
        try:
            pet_data = TestDataGenerator.generate_pet_data()
            with self.client.post(
                "/pet",
                json=pet_data,
                headers=Config.HEADERS,
                catch_response=True
            ) as response:
                if response.status_code == 200:
                    self.pet_ids.add(pet_data["id"])
                    try:
                        response_json = response.json()
                        assert response_json["id"] == pet_data["id"], f"Eklenen pet ID'si beklenenden farklı: {response_json['id']}"
                        assert response_json["name"] == pet_data["name"], f"Eklenen pet adı beklenenden farklı: {response_json['name']}"
                        assert response_json["status"] == pet_data["status"], f"Eklenen pet durumu beklenenden farklı: {response_json['status']}"
                        pass 
                    except (json.JSONDecodeError, AssertionError) as e:
                        response.failure(f"Eklenen pet yanıtı doğrulanamadı: {e}")
                        logger.error(f"Eklenen pet yanıtı doğrulanamadı: {e}")
                else:
                    response.failure(f"Pet eklenemedi (Durum Kodu: {response.status_code}): {response.text}")
                    logger.error(f"Pet eklenemedi (Durum Kodu: {response.status_code}): {response.text}")
        except Exception as e:
            logger.error(f"Pet eklenirken hata: {str(e)}")

    @task(Config.SCENARIO_WEIGHTS["get_pet"])
    def get_pet_by_id(self):
        """ID'ye göre pet bilgilerini getir"""
        if not self.pet_ids:
            self._create_initial_pet()
            return

        try:
            pet_id = random.choice(list(self.pet_ids))
            with self.client.get(
                f"/pet/{pet_id}",
                headers=Config.HEADERS,
                catch_response=True,
                name="/pet/:id"
            ) as response:
                if response.status_code == 200:
                    try:
                        response_json = response.json()
                        assert response_json["id"] == pet_id, f"Getirilen pet ID'si beklenenden farklı: {response_json['id']}"
                        pass 
                    except (json.JSONDecodeError, AssertionError) as e:
                        response.failure(f"Getirilen pet yanıtı doğrulanamadı: {e}")
                        logger.error(f"Getirilen pet yanıtı doğrulanamadı: {e}")
                else:
                    response.failure(f"Pet getirilemedi (Durum Kodu: {response.status_code}): {response.text}")
                    logger.error(f"Pet getirilemedi (Durum Kodu: {response.status_code}): {response.text}")
                    # Eğer pet bulunamadıysa, ID'yi listeden kaldır
                    if response.status_code == 404:
                        self.pet_ids.remove(pet_id)
        except Exception as e:
            logger.error(f"Pet getirilirken hata: {str(e)}")

    @task(Config.SCENARIO_WEIGHTS["update_pet"])
    def update_pet(self):
        """Mevcut bir peti güncelle"""
        if not self.pet_ids:
            self._create_initial_pet()
            return

        try:
            pet_id = random.choice(list(self.pet_ids))
            pet_data = TestDataGenerator.generate_pet_data(pet_id)
            
            with self.client.put(
                "/pet",
                json=pet_data,
                headers=Config.HEADERS,
                catch_response=True,
                name="/pet/:id"
            ) as response:
                if response.status_code == 200:
                    try:
                        response_json = response.json()
                        assert response_json["id"] == pet_data["id"], f"Güncellenen pet ID'si beklenenden farklı: {response_json['id']}"
                        assert response_json["name"] == pet_data["name"], f"Güncellenen pet adı beklenenden farklı: {response_json['name']}"
                        assert response_json["status"] == pet_data["status"], f"Güncellenen pet durumu beklenenden farklı: {response_json['status']}"
                        pass 
                    except (json.JSONDecodeError, AssertionError) as e:
                        response.failure(f"Güncellenen pet yanıtı doğrulanamadı: {e}")
                        logger.error(f"Güncellenen pet yanıtı doğrulanamadı: {e}")
                else:
                    response.failure(f"Pet güncellenemedi (Durum Kodu: {response.status_code}): {response.text}")
                    logger.error(f"Pet güncellenemedi (Durum Kodu: {response.status_code}): {response.text}")
                    # Eğer pet bulunamadıysa, ID'yi listeden kaldır
                    if response.status_code == 404:
                        self.pet_ids.remove(pet_id)
        except Exception as e:
            logger.error(f"Pet güncellenirken hata: {str(e)}")

    @task(Config.SCENARIO_WEIGHTS["delete_pet"])
    def delete_pet(self):
        """Bir peti sil"""
        if not self.pet_ids:
            self._create_initial_pet()
            return

        try:
            pet_id = random.choice(list(self.pet_ids))
            with self.client.delete(
                f"/pet/{pet_id}",
                headers=Config.HEADERS,
                catch_response=True,
                name="/pet/:id"
            ) as response:
                if response.status_code == 200:
                    self.pet_ids.remove(pet_id)
                    pass 
                else:
                    response.failure(f"Pet silinemedi (Durum Kodu: {response.status_code}): {response.text}")
                    logger.error(f"Pet silinemedi (Durum Kodu: {response.status_code}): {response.text}")
                    # Eğer pet bulunamadıysa, ID'yi listeden kaldır
                    if response.status_code == 404:
                        self.pet_ids.remove(pet_id)
        except Exception as e:
            logger.error(f"Pet silinirken hata: {str(e)}")

    def on_stop(self):
        """Test durduğunda veya bittiğinde temizlik yap"""
        # Oluşturulan tüm petleri temizle
        logger.info(f"Kullanıcı duruyor. Toplam {len(self.pet_ids)} pet temizlenecek.")
        for pet_id in list(self.pet_ids): # Set üzerinde dönerken değişiklik yapmamak için kopyasını al
            try:
                with self.client.delete(
                    f"/pet/{pet_id}",
                    headers=Config.HEADERS,
                    catch_response=True,
                    name="/pet/:id (cleanup)" # Temizlik isteklerini ayrı isimlendir
                ) as response:
                    if response.status_code == 200:
                        self.pet_ids.remove(pet_id)
                        logger.info(f"Pet ID {pet_id} başarıyla temizlendi.")
                    elif response.status_code == 404:
                        self.pet_ids.remove(pet_id)
                        logger.warning(f"Pet ID {pet_id} zaten mevcut değil (404), listeden kaldırıldı.")
                    else:
                        response.failure(f"Pet ID {pet_id} temizlenemedi (Durum Kodu: {response.status_code}): {response.text}")
                        logger.error(f"Pet ID {pet_id} temizlenirken hata (Durum Kodu: {response.status_code}): {response.text}")
            except Exception as e:
                logger.error(f"Pet ID {pet_id} temizlenirken beklenmeyen hata: {str(e)}")
        
