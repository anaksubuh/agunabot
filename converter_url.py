import os
import time
import json
import sys
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def url_produk_split(url_produk_split):

    # === Konfigurasi Chrome ===
    profile_path = os.path.abspath("profile/shopee")
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={profile_path}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--silent")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("detach", True)
    sys.stderr = open(os.devnull, "w")

    hiden = 0
    if hiden == 1:
        chrome_options.add_argument("--headless=new")  # Mode headless versi baru

    # === Inisialisasi Driver ===
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url_produk_split = url_produk_split.split('https')

    for i in range(10):
        i = i+1
        url_produk = url_produk_split[i]
        url_produk = f'https://shopee.co.id/{url_produk}'
        try:
            print(url_produk)
        except:
            break

        driver.get('https://affiliate.shopee.co.id/offer/custom_link')


        while True:
            try:
                driver.find_element(By.XPATH,'/html/body/div[2]/section/section/section/main/div[2]/div[1]/div[2]/div[2]/form/div[1]/div/div/span/div/textarea').send_keys(url_produk)
            except:
                continue
            else:
                break
        driver.find_element(By.XPATH,'/html/body/div[2]/section/section/section/main/div[2]/div[1]/div[2]/div[2]/form/div[2]/div[2]/div/span/input').send_keys('ROBOT')
        driver.find_element(By.XPATH,'/html/body/div[2]/section/section/section/main/div[2]/div[1]/div[2]/div[2]/form/div[7]/div/div/span/button').click()
        time.sleep(0.1)

        while True:
            try:
                xpath_list = [
                    '/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div/textarea',
                    '/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div',
                    '/html/body/div[5]/div/div[2]/div/div[2]/div[1]',
                    '/html/body/div[5]/div/div[2]/div/div[2]',
                    '/html/body/div[5]/div/div[2]/div',
                ]
                for xpath in xpath_list:
                    try:
                        url_final = driver.find_element(By.XPATH, xpath).text
                        url_final = url_final.replace('Link dari Link Khusus (Custom Link)','')
                        url_final = url_final.replace('Mohon salin link singkat','')
                        url_final = url_final.replace('Salin Link','')
                    except NoSuchElementException:
                        continue
            except:
                continue
            else:
                break

        # === Replace url_produk dengan url_final di deskripsi.txt ===
        try:
            with open("deskripsi.txt", "r", encoding="utf-8") as f:
                content = f.read()

            # Pastikan URL asli yang dicetak sebelumnya digunakan untuk replace
            content = content.replace(url_produk, url_final)

            with open("deskripsi.txt", "w", encoding="utf-8") as f:
                f.write(content)

            print(f"[✔] URL diganti di deskripsi.txt: {url_produk} → {url_final}")
        except Exception as e:
            print(f"[❌] Gagal mengganti URL di deskripsi.txt: {e}")

        with open("url_mapping.txt", "a", encoding="utf-8") as log:
            log.write(f"{url_produk} → {url_final}\n")

        print(url_final)

import re

def extract_urls_from_deskripsi(file_path):
    file_path = 'deskripsi.txt'
    if not os.path.exists(file_path):
        print(f"[❌] File tidak ditemukan: {file_path}")
        return ""

    urls = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            found = re.findall(r"https?://\S+", line)
            urls.extend(found)

    # Gabungkan semua URL jadi satu string tanpa separator
    return "".join(urls)

# === Contoh penggunaan ===
if __name__ == "__main__":
    file_deskripsi = "deskripsi.txt"
    hasil = extract_urls_from_deskripsi(file_deskripsi)
    print(f"[✔] URL gabungan:\n{hasil}")
