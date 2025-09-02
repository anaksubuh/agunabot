import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def autologin(username, password):
    username = str(username)
    password = str(password)

    # Setup Chrome
    profile_path = f"D:\\Master twitter\\profile\\{username}"
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
    driver.get(f"https://x.com/{username}")
    time.sleep(3)

    def delay():
        time.sleep(random.uniform(2, 4))

    name = "N/A"
    scraped_username = username
    following = "N/A"
    followers = "N/A"

    try:
        # Cek apakah belum login
        login_button = driver.find_element(By.XPATH, '//a[@href="/login"]')
        login_button.click()
        print("[!] Belum login, lanjutkan proses login...")
        delay()

        # Masukkan username
        try:
            username_input = driver.find_element(By.XPATH, '//input[@autocomplete="username"]')
            username_input.click()
            username_input.send_keys(username)
            print("[✔] Username dimasukkan")
            delay()
        except Exception as e:
            print(f"[❌] Gagal input username: {e}")

        # Klik tombol Next
        try:
            next_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div')
            next_button.click()
            print("[✔] Tombol Next diklik")
            delay()
        except Exception as e:
            print(f"[❌] Gagal klik tombol Next: {e}")

        # Masukkan password
        try:
            password_input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
            password_input.click()
            password_input.send_keys(password)
            print("[✔] Password dimasukkan")
            delay()
        except Exception as e:
            print(f"[❌] Gagal input password: {e}")

        # Klik tombol Login
        try:
            login_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button/div')
            login_button.click()
            print("[✔] Login berhasil diklik")
            delay()
        except Exception as e:
            print(f"[❌] Gagal klik tombol login: {e}")

        time.sleep(10)

    except Exception as e:
        print(f"[✓] Sudah login atau tidak perlu login: {e}")

    # Ambil data
    try:
        img_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/a/div[3]/div/div[2]/div/img')
        img_src = img_element.get_attribute("src")
    except:
        img_src = "N/A"

    try:
        name = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div/div/span').text
    except:
        name = "N/A"

    try:
        scraped_username = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div/div/div/span').text
    except:
        scraped_username = username

    try:
        following = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div[1]/div[2]/div[4]/div[1]/a/span[1]/span').text
    except:
        following = "N/A"

    try:
        followers = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div[1]/div[2]/div[4]/div[2]/a/span[1]/span').text
    except:
        followers = "N/A"

    output_line = f"{name}|{scraped_username}|{password}|{following}|{followers}|valid"
    file_path = "profil_output.txt"

    # Cek apakah baris sudah ada
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            existing_lines = [line.strip() for line in f.readlines()]
    else:
        existing_lines = []

    # Tambahkan jika belum ada
    if output_line not in existing_lines:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(output_line + "\n")
        print("[✔] Data baru ditambahkan ke profil_output.txt")
    else:
        print("[✓] Data sudah ada, tidak ditambahkan ulang.")

    driver.quit()

autologin("ivenuemart", "akukamudia12345")