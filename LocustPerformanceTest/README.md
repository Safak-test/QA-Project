# Locust PetStore API Performans Testi

Bu proje, Locust yük testi aracı kullanılarak bir PetStore API'sinin performansını test etmek için geliştirilmiştir. Çeşitli API endpoint'lerine yük bindirerek sistemin stres ve stabilite altındaki davranışını ölçmeyi hedefler.

## Özellikler

*   **Dinamik Veri Yönetimi:** Her sanal kullanıcı için başlangıçta pet verileri oluşturularak, test senaryolarının tutarlı çalışması sağlanır ve özellikle GET/DELETE operasyonlarında yaşanabilecek başlangıç 404 hatalarının önüne geçilir. Test süresince eğer gerekiyorsa dinamik olarak yeni pet verileri oluşturulmaya ve kullanılmaya devam edilir.
*   **Gelişmiş Hata Yakalama:** İstek hataları (örn. 404 Not Found) yakalanır, loglanır ve Locust istatistiklerine yansıtılır.Başarılı geçen testleri loglama kısmında fazla dağınıklık olmaması adına loglama kısmında görüntülemiyoruz.
*   **Yanıt Doğrulama:** API yanıtları, beklenen veri tutarlılığı ve doğruluğu için `assert` ifadeleri kullanılarak detaylıca doğrulanır.
*   **Merkezi Yapılandırma:** `config.py` dosyası aracılığıyla temel URL, bekleme süreleri, HTTP başlıkları ve senaryo ağırlıkları gibi tüm kritik test parametreleri merkezi bir yerden kolayca yönetilebilir.
*   **Detaylı Loglama:** `INFO` seviyesinde yapılandırılmış loglama sayesinde, test akışı ve potansiyel sorunlar hakkında daha fazla görünürlük sağlanır.
*   **Temiz Kapanış:** Test bittiğinde veya durduğunda, oluşturulan tüm petlerin API'den temizlenmesi sağlanır.

## Kurulum

Projeyi çalıştırmak için aşağıdaki adımları izleyin:

1.  **Python Kurulumu:** Sisteminizde Python 3.x kurulu olduğundan emin olun.
2.  **Bağımlılıkları Yükleme:** Proje dizinine gidin ve gerekli Python kütüphanelerini yükleyin:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Yapılandırma:**
    *   `config.py` dosyasını PetStore API'nizin temel URL'si (`BASE_URL`), HTTP başlıkları (`HEADERS`) ve senaryo ağırlıkları (`SCENARIO_WEIGHTS`) ile güncelleyin.
    *   `test_data.py` dosyasını test verisi oluşturma mantığınıza göre düzenleyin.

## Kullanım

Locust testini başlatmak için, kolaylık sağlaması amacıyla oluşturulan aşağıdaki batch dosyasını kullanabilirsiniz. Güvenlik nedeniyle, herhangi bir yürütülebilir dosyayı çalıştırmadan önce her zaman içeriğini bir metin düzenleyiciyle (örneğin Not Defteri) incelemeniz önerilir. `run_locust.bat` dosyasının içeriği tamamen şeffaf ve zararsızdır.

```bash
.\run_locust.bat
```

Bu komut, Locust sunucusunu yeni bir pencerede başlatacak ve ardından varsayılan tarayıcınızda Locust web arayüzünü (`http://localhost:8089`) otomatik olarak açacaktır. Testi durdurmak için Locust sunucusunun çalıştığı CMD penceresini kapatmanız yeterlidir.

Alternatif olarak, batch dosyasını kullanmak istemiyorsanız, Locust testini doğrudan aşağıdaki komutla başlatabilirsiniz:

```bash
locust -f Main.py
```

## Test Senaryoları

Bu proje aşağıdaki PetStore API endpoint'lerini test eder:

*   `POST /pet`: Yeni bir pet ekler.
*   `GET /pet/:id`: Belirli bir pet ID'sine göre pet bilgilerini getirir.
*   `PUT /pet`: Mevcut bir peti günceller.
*   `DELETE /pet/:id`: Belirli bir pet ID'sini siler.

## Loglama ve Hata Yönetimi

Loglama seviyesi `INFO` olarak ayarlanmıştır. Bu, Locust'un ana loglarına `INFO`, `WARNING`, `ERROR` ve `CRITICAL` seviyesindeki mesajların yazılacağı anlamına gelir. Özellikle GET ve DELETE operasyonlarında karşılaşılan 404 (Not Found) hataları, test ortamındaki veri tutarsızlıkları ve eşzamanlılık sorunları hakkında önemli bilgiler sağlamak amacıyla loglanır. Test sonrası temizlik adımı da loglanır. 