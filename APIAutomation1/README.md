# Python API Otomasyon Çerçevesi

Bu proje, Python, Pytest ve Allure Report kullanarak geliştirilmiş  bir API otomasyon çerçevesidir. Dinamik test verisi üretimi, yapılandırılmış test senaryoları ve detaylı raporlama ile API test süreçlerini optimize etmeyi amaçlamaktadır.

## İçindekiler
- [Proje Yapısı](#proje-yapısı)
- [Temel Özellikler](#temel-özellikler)
- [Kurulum Rehberi](#kurulum-rehberi)
- [Testleri Çalıştırma](#testleri-çalıştırma)
- [Allure Raporlama](#allure-raporlama)
- [Bilinen Hatalar](#bilinen-hatalar)

## Proje Yapısı

```
APIAutomation/
├── config/
│   └── settings.py           # API URL'leri, HTTP başlıkları, test verileri ve framework ayarları
├── base/
│   ├── base_library.py       # Temel HTTP istek metodları ve Allure entegrasyonu
│   └── base_test.py          # Test sınıfları için temel sınıf ve ortak metodlar
├── tests/
│   └── test_user.py          # Kullanıcı yönetimi API test senaryoları
├── utils/
│   └── data_generator.py     # Dinamik test verisi üretimi
├── .venv/                    # Python sanal ortam
├── allure-results/           # Allure test sonuçları
├── allure-report/            # Allure HTML raporu
├── run_tests.py              # Test çalıştırma ve rapor oluşturma scripti
├── conftest.py               # Pytest konfigürasyonları
└── requirements.txt          # Proje bağımlılıkları
```

## Temel Özellikler

* **Dinamik Test Verisi Üretimi**: Faker kütüphanesi ile gerçekçi test verileri
* **Kapsamlı Allure Raporlama**:
  * Detaylı test adımları ve istek/yanıt bilgileri
  * Epic, Feature, Suite, Severity etiketleri
  * Otomatik rapor temizleme ve oluşturma
* **Esnek Retry Mekanizması**: Yapılandırılabilir API istek yeniden deneme
* **Merkezi Yapılandırma**: Tek noktadan yönetilen test ve çevre ayarları
* **Paralel Test Çalıştırma**: pytest-xdist ile hızlı test execution
* **Akıllı Test Yönetimi**:
  * **Bağımsız Test Senaryoları**: Her test kendi verilerini oluşturur ve yönetir
  * **Otomatik Test Hazırlığı**: Her test öncesi otomatik kullanıcı oluşturma
  * **Akıllı Yeniden Deneme**: Başarısız istekleri yapılandırılabilir sayıda otomatik tekrarlama
  * **Hata Toleransı**: Bilinen API kısıtlamalarına karşı otomatik iyileştirmeler

## Kurulum Rehberi

### Önkoşullar

* **Python 3.8+**
* **pip** (Python paket yöneticisi)
* **Git** (versiyon kontrolü için)
* **Allure Commandline**: [Resmi kurulum rehberi](https://docs.qameta.io/allure/#_installing_a_commandline)

### Kurulum Adımları

1. **Projeyi Klonlayın**:
   ```bash
   git clone <proje-depo-adresi>
   cd APIAutomation
   ```

2. **Sanal Ortam Oluşturun ve Aktive Edin**:
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Bağımlılıkları Yükleyin**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Allure CLI Kurulumu**:
   ```bash
   # Windows (Scoop ile)
   scoop install allure

   # macOS (Homebrew ile)
   brew install allure

   # Linux (apt ile)
   sudo apt-add-repository ppa:qameta/allure
   sudo apt-get update
   sudo apt-get install allure
   ```

## Testleri Çalıştırma

### Tüm Testleri Çalıştırma

```bash
python run_tests.py
```

Bu komut:
* Mevcut Allure sonuçlarını temizler
* Testleri çalıştırır
* Allure raporunu otomatik oluşturur ve açar

### Belirli Testleri Çalıştırma

```bash
# Belirli bir test dosyası
pytest tests/test_user.py -v

# Belirli bir test fonksiyonu
pytest tests/test_user.py::test_create_user -v

```

### CI/CD Ortamında Çalıştırma

```bash
pytest tests/ --alluredir=./allure-results -v
allure generate ./allure-results -o ./allure-report --clean
```

## Allure Raporlama

### Rapor Oluşturma

```bash
# Rapor oluşturma ve görüntüleme
allure serve ./allure-results

# Statik rapor oluşturma
allure generate ./allure-results -o ./allure-report --clean
```

### Rapor İçeriği
* Test durumları ve sonuçları
* Detaylı test adımları
* İstek/yanıt bilgileri
* Test süreleri ve performans metrikleri
* Özel etiketler ve kategoriler

## Bilinen Hatalar

* **DELETE ve GET İşlemi İdempotent Değil (Bug ID: PS-108,PS-107)**: API'nin DELETE ve GET endpoint'leri REST API prensiplerine aykırı olarak idempotent değildir. Silinen kaynaklar için tekrar DELETE ve GET istekleri 404 hatası döndürmektedir.

