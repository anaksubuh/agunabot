import os
import time
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os, sys

def scraptread(st,url):

    username = "mylove1220367"  # Ganti dengan username yang diinginkan

    # === Bangun path dinamis ===
    profile_path = f"D:\\Master twitter\\profile\\{username}"
    st.write(f"[+] Menggunakan akun: {username}")
    upload_txt_path = os.path.join("D:\\Master twitter\\profile\\upload.txt")
    video_folder = os.path.join("D:\\Master twitter\\profile\\downloaded_photo\\")

    # Konfigurasi ChromeOptions

    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={profile_path}")       # Gunakan profil Chrome
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")  
    chrome_options.add_argument("--silent")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("detach", True)
    service = Service("chromedriver.exe", log_path="NUL")
    sys.stderr = open(os.devnull, "w")

    # Mode headless kalau dibutuhkan
    hiden = 1
    if hiden == 1:
        chrome_options.add_argument("--headless=new")  # Mode headless versi baru

    # Gunakan webdriver-manager untuk otomatis handle ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    for i in range(0):
        driver.quit()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

    id_post = url.split("/")[-1]

    driver.get(url)

    time.sleep(3)

    def scroll_to_bottom():
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    #scroll_to_bottom()

    def deskripsi_header():
        try:
            header = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[1]/div/div')
            print(header.text)
            st.write(header.text)
            return header.text
        except Exception as e:
            print(f"Error finding header: {e}")
            st.write(f"Error finding header: {e}")
            return None


    def image_header_to_json(tweet_id):
        try:
            tweets = driver.find_elements(By.XPATH, '//article[@role="article"]')

            if not tweets:
                print("[ERROR] Tidak ada tweet ditemukan")
                st.write("[ERROR] Tidak ada tweet ditemukan")
                return {}

            # Struktur data tweet
            tweet_data = {
                "header": {
                    "deskripsi": "",
                    "image": []
                },
                "threads": []
            }

            def is_valid_image(url):
                """Filter gambar: hindari .svg dan profile_images"""
                return (
                    url and
                    ".svg" not in url and
                    "profile_images" not in url
                )

            for i, tweet in enumerate(tweets):
                try:
                    # Ambil teks
                    try:
                        text_elem = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
                        deskripsi = text_elem.text.strip()
                    except:
                        deskripsi = "[Tidak ada teks]"

                    # Ambil gambar dan filter
                    img_elems = tweet.find_elements(By.XPATH, './/img[contains(@src, "twimg")]')
                    img_urls = [
                        img.get_attribute("src")
                        for img in img_elems
                        if is_valid_image(img.get_attribute("src"))
                    ]

                    if i == 0:
                        tweet_data["header"]["deskripsi"] = deskripsi
                        tweet_data["header"]["image"] = img_urls
                    else:
                        tweet_data["threads"].append({
                            "deskripsi": deskripsi,
                            "image": img_urls
                        })

                except Exception as e:
                    print(f"[WARNING] Gagal parsing tweet ke-{i}: {e}")
                    st.write(f"[WARNING] Gagal parsing tweet ke-{i}: {e}")

            # Simpan ke database.json
            db_path = "database.json"
            if os.path.exists(db_path):
                with open(db_path, "r", encoding="utf-8") as f:
                    database = json.load(f)
            else:
                database = {}

            if tweet_id not in database:
                database[tweet_id] = tweet_data
                with open(db_path, "w", encoding="utf-8") as f:
                    json.dump(database, f, indent=2, ensure_ascii=False)
                print(f"[+] Data tweet ID {tweet_id} berhasil ditambahkan ke database.json")
                st.write(f"[+] Data tweet ID {tweet_id} berhasil ditambahkan ke database.json")
            else:
                print(f"[INFO] Data tweet ID {tweet_id} sudah ada, tidak ditambahkan ulang")
                st.write(f"[INFO] Data tweet ID {tweet_id} sudah ada, tidak ditambahkan ulang")

            return tweet_data

        except Exception as e:
            print(f"[ERROR] Gagal mengambil gambar: {e}")
            st.write(f"[ERROR] Gagal mengambil gambar: {e}")
            return 


    deskripsi_header()
    image_header_to_json(f"{id_post}")
    driver.quit()