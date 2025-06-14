# Python API Otomasyon Çerçevesi

Bu proje, Python, Pytest ve Allure Report kullanarak geliştirilmiş kapsamlı bir API otomasyon çerçevesidir. Dinamik test verisi üretimi, yapılandırılmış test senaryoları ve detaylı raporlama yetenekleri ile API test süreçlerini optimize etmeyi amaçlamaktadır.

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
│   └── settings.py           # API URL'leri, HTTP başlıkları, test verileri ve framework ayarları gibi tüm yapılandırma parametrelerini merkezi olarak içerir.
├── base/
│   ├── base_library.py       # Temel HTTP istek metodlarını (GET, POST, PUT, DELETE) ve Allure entegrasyonu ile detaylı istek/yanıt loglamasını sağlar.
│   └── base_test.py          # Tüm test sınıfları için ortak bir temel sınıf sunar. Bu sınıf, test öncesi (setup) ve sonrası (teardown) işlemleri, ortak yardımcı metodları ve genel test yapılandırmasını yönetir.
├── tests/
│   └── test_user.py          # Kullanıcı oluşturma, getirme, güncelleme, silme, giriş yapma ve çıkış yapma gibi kullanıcı yönetimi API operasyonlarına yönelik test senaryolarını barındırır. Her senaryo, Allure ile detaylı raporlama için zenginleştirilmiştir.
├── utils/
│   └── data_generator.py     # Dinamik ve gerçekçi test verileri (kullanıcı bilgileri gibi) üretmek için `Faker` kütüphanesini kullanır. Testlerin her çalışmasında benzersiz verilerle doğrulama yapılmasını sağlar.
├── venv/                     # Python sanal ortam dizini.
├── .pytest_cache/            # Pytest önbellek dizini.
├── allure-results/           # Allure ham test sonuçları.
├── allure-report/            # Oluşturulan Allure HTML raporu.
├── run_tests.py              # Test çalıştırma ve Allure raporu başlatma scripti.
├── conftest.py               # Pytest konfigürasyonları ve fixture tanımları.
└── requirements.txt          # Proje bağımlılıkları listesi.
```

## Temel Özellikler

*   **Dinamik Test Verisi Üretimi**: `Faker` kütüphanesi ile gerçekçi ve değişken test verileri oluşturulur.
*   **Yapılandırılmış Test Senaryoları**: `Pytest` kullanarak testler modüler ve okunabilir bir yapıda yazılmıştır.
*   **Kapsamlı Allure Raporlama**:
    *   Detaylı test adımları, istek/yanıt bilgileri Allure raporlarına eklenir.
    *   Test raporları `Epic`, `Feature`, `Suite`, `Severity` gibi etiketlerle zenginleştirilmiştir.
    *   Her test çalıştırması öncesi eski sonuçlar otomatik olarak temizlenir.
*   **Esnek Retry Mekanizması**: API istekleri için yapılandırılabilir yeniden deneme mekanizması entegre edilmiştir.
*   **Merkezi Yapılandırma**: Tüm çevresel ve test ayarları `config/settings.py` dosyasında merkezi olarak yönetilir.
*   **Modüler ve Genişletilebilir Mimari**: Yeni API endpoint'leri ve test senaryolarının eklenmesi kolaydır.

## Kurulum Rehberi

Projeyi yerel ortamınızda kurmak için aşağıdaki adımları takip edin:

### Önkoşullar

*   **Python 3.8+**
*   **pip** (Python paket yöneticisi)
*   **Allure Commandline**: Allure CLI kurulumu için [resmi dökümantasyonu](https://docs.qameta.io/allure/#_installing_a_commandline) inceleyiniz.

### Kurulum Adımları

1.  **Projeyi Klonlayın**:
    ```bash
    git clone <proje-depo-adresi>
    cd APIAutomation
    ```

2.  **Sanal Ortam Oluşturun ve Aktive Edin**:
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Bağımlılıkları Yükleyin**:
    ```bash
    pip install -r requirements.txt
    ```

## Testleri Çalıştırma

Tüm testleri çalıştırmak ve Allure raporunu otomatik olarak oluşturup görüntülemek için `run_tests.py` script'ini kullanın:

```bash
python run_tests.py
```

Bu kod ile, mevcut Allure sonuç ve rapor dizinlerini temizler, testleri çalıştırır ve testler tamamlandıktan sonra Allure raporunu web tarayıcısında otomatik olarak açar.

### CI/CD Ortamında Test Çalıştırma

CI/CD ortamlarında (örn. Jenkins, GitLab CI, GitHub Actions) Allure raporunun otomatik oluşumu `conftest.py` dosyası üzerinden yönetilir. Genellikle sadece `pytest` komutunu çalıştırmanız yeterlidir:

```bash
pytest tests/test_user.py --alluredir=./allure-results -v
```

## Allure Raporlama

Test çalıştırmaları sonrası `allure-report` dizininde detaylı ve etkileşimli bir rapor bulunur. Bu rapor, test durumlarını, adım detaylarını, istek/yanıt bilgilerini ve diğer önemli metrikleri görsel olarak sunar.

## Bilinen Hatalar

*   **DELETE İşlemi İdempotent Değil (Bug ID: PS-108)**: API'nin DELETE endpoint'i, REST API prensiplerine aykırı olarak idempotent değildir. Bir kaynağın silinmesinden sonra aynı DELETE isteği tekrar gönderildiğinde 404 hatası alınmaktadır. İdempotent işlemler, birden fazla kez tekrarlansa bile sistemde aynı etkiyi yaratmalıdır. Bu durum `tests/test_user.py` içindeki `test_delete_user` metodunda belirtilmiştir. 