import os
import subprocess
import webbrowser
import shutil

def run_tests():
    """
    Testleri çalıştırır ve Allure raporunu oluşturur.
    """
    print("\n--- Eski Allure Sonuçlarını Temizle ---")
    if os.path.exists("./allure-results"):
        shutil.rmtree("./allure-results")
        print("allure-results klasörü temizlendi.")
    os.makedirs("./allure-results", exist_ok=True)
    print("allure-results klasörü oluşturuldu.")

    print("\n--- Pytest Testlerini Çalıştır ---")
    # Testleri çalıştır
    pytest_command = ["pytest", "tests/test_user.py", "--alluredir=./allure-results", "-v", "-n", "auto"]
    print(f"Çalıştırılan komut: {' '.join(pytest_command)}")
    subprocess.run(pytest_command, check=True)
    print("Pytest testleri tamamlandı.")

    print("\n--- allure-results Klasör İçeriği ---")
    if os.path.exists("./allure-results"):
        results_files = os.listdir("./allure-results")
        if results_files:
            print(f"allure-results klasöründe {len(results_files)} dosya bulundu:")
            for f in results_files:
                print(f"  - {f}")
        else:
            print("allure-results klasörü boş.")
    else:
        print("allure-results klasörü bulunamadı!")

    print("\n--- Allure Raporunu Sunucu Üzerinde Aç ---")
    # Allure raporunu sunucu üzerinde aç
    try:
        allure_serve_command = "allure serve ./allure-results"
        print(f"Çalıştırılan komut: {allure_serve_command}")
        # allure serve komutu tarayıcıyı otomatik açar ve sunucuyu başlatır.
        subprocess.Popen(allure_serve_command, shell=True)
        print("Allure raporu sunucu üzerinde başlatıldı ve tarayıcınızda açılıyor olmalı.")
    except Exception as e:
        print(f"Hata: Allure raporunu sunucu üzerinde başlatma başarısız oldu: {e}")
        print("Lütfen Allure command-line aracının doğru yüklendiğinden ve PATH'te olduğundan emin olun.")

if __name__ == "__main__":
    run_tests() 