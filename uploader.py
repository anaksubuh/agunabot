import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome
profile_path = "D:\\Master twitter\\profile\\mylove1220367"
base_path = "D:\\Master twitter\\downloaded_images\\"

chrome_options = Options()
chrome_options.add_argument(f"user-data-dir={profile_path}")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get('https://x.com/home')
time.sleep(3)

# Helper
def delay():
    time.sleep(random.uniform(2, 5))

def type_slow(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))

# Load deskripsi.txt
with open("deskripsi.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

# Proses setiap baris
for index, line in enumerate(lines):
    jumlah_gambar, deskripsi = line.split("|")
    jumlah_gambar = int(jumlah_gambar)

    # Upload gambar-gambar
    for i in range(1, jumlah_gambar + 1):
        if index == 0:
            img_path = f"{base_path}header{i}.jpg"
        else:
            img_path = f"{base_path}gambar{index}.{i}.jpg"

        try:
            upload_image = driver.find_element(By.XPATH, "//input[@type='file']")
            upload_image.send_keys(img_path)
            print(f"[✔] Upload gambar: {img_path}")
            delay()
        except Exception as e:
            print(f"[❌] Gagal upload gambar {img_path}: {e}")

    # Isi deskripsi
    try:
        if index == 0:
            xpath_deskripsi = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div/div/div'
        else:
            xpath_deskripsi = f'/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[{index+1}]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div'

        deskripsi_field = driver.find_element(By.XPATH, xpath_deskripsi)
        type_slow(deskripsi_field, deskripsi)
        print(f"[✔] Deskripsi konten ke-{index}: {deskripsi}")
        delay()
    except Exception as e:
        print(f"[❌] Gagal input deskripsi konten ke-{index}: {e}")

    # Tambah konten (kecuali terakhir)
    try:
        if index < len(lines) - 1:  # hanya klik tambah jika masih ada baris berikutnya
            if index == 0:
                tambah_xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/a/div'
            else:
                tambah_xpath = f'/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[{index+1}]/div/div/div/div[2]/div[2]/div/div/div/button[1]'

            driver.find_element(By.XPATH, tambah_xpath).click()
            print(f"[+] Tambah konten setelah konten ke-{index}")
            delay()
        else:
            print(f"[✓] Konten terakhir, tidak perlu tambah konten lagi.")
    except Exception as e:
        print(f"[❌] Gagal tambah konten ke-{index}: {e}")

# Final upload
try:
    final_xpath = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[3]/div/div/div/div[2]/div[2]/div/div/div/button[2]/div'
    driver.find_element(By.XPATH, final_xpath).click()
    print("[✔] Upload final berhasil")
except Exception as e:
    print(f"[❌] Gagal upload final: {e}")
