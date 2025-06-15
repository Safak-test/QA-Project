@echo off
echo Locust performans testini baslatiliyor...

REM Locust'u yeni bir CMD penceresinde baslat
REM Bu pencere, Locust sunucusu calistigi surece acik kalacaktir.
start "Locust Server" cmd /c "locust -f Main.py"

echo Locust sunucusunun baslamasi bekleniyor... (5 saniye)
timeout /t 5 /nobreak > nul

echo Tarayici aciliyor...
start http://localhost:8089

echo Teste baslamak icin Locust web arayuzunu kullanabilirsiniz.
echo Locust sunucusunu durdurmak icin Locust Server penceresini kapatin veya Ctrl+C kullanin.
pause 