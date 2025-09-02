import os
import re
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def delay():
    time.sleep(random.uniform(2, 4))

def type_slow(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))

def process_upload(username, idpost):
    profile_path = f"D:/Master twitter/profile/{username}"

    # === Jalankan modul scraping dan database ===
    import download_image
    download_image.scrap_gambar(idpost)

    import get_database
    get_database.get_database_entry(idpost)

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
        import converter_url
        converter_url.url_produk_split(hasil)

    # === Load deskripsi.txt ===
    if not os.path.exists("deskripsi.txt"):
        print("[❌] File deskripsi.txt tidak ditemukan.")
        return

    with open("deskripsi.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if "|" in line]

    # === Setup Chrome ===
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
    driver.get("https://x.com/home")
    time.sleep(3)

    # === Proses setiap baris deskripsi ===
    for index, line in enumerate(lines):
        try:
            jumlah_gambar, deskripsi = line.split("|", 1)
            jumlah_gambar = int(jumlah_gambar)
        except:
            print(f"[⚠] Format tidak valid di baris {index}: {line}")
            continue

        # === Upload gambar ===
        for i in range(1, jumlah_gambar + 1):
            if index == 0:
                img_path = f"D:\\Master twitter\\downloaded_images\\header{i}.jpg"
            else:
                img_path = f"D:\\Master twitter\\downloaded_images\\gambar{index}.{i}.jpg"

            # Validasi file sebelum upload
            if not os.path.exists(img_path):
                print(f"[⚠️] File tidak ditemukan: {img_path}")
                continue

            try:
                # Temukan elemen input file (bukan tombol atau ikon SVG)
                upload_input = driver.find_element(By.XPATH, '//input[@type="file"]')

                # Kirim path gambar ke input file
                upload_input.send_keys(img_path)
                print(f"[✔] Upload gambar: {img_path}")
                delay()

            except Exception as e:
                print(f"[❌] Gagal upload gambar {img_path}: {e}")

        # === Isi deskripsi ===
        try:
            if index == 0:
                xpath_deskripsi = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div/div/div'
            else:
                xpath_deskripsi = f'/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[{index+1}]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div'

            deskripsi_field = driver.find_element(By.XPATH, xpath_deskripsi)
            deskripsi_clean = deskripsi.replace("~", "\n")
            type_slow(deskripsi_field, deskripsi_clean)
            print(f"[✔] Deskripsi konten ke-{index}: {deskripsi_clean}")
            delay()
        except Exception as e:
            print(f"[❌] Gagal input deskripsi konten ke-{index}: {e}")


        # === Tambah konten jika belum terakhir ===
        try:
            if index < len(lines) - 1:
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

    # === Final upload ===
    try:
        final_xpath = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[3]/div/div/div/div[2]/div[2]/div/div/div/button[2]/div'
        driver.find_element(By.XPATH, final_xpath).click()
        print("[✔] Upload final berhasil")
    except Exception as e:
        print(f"[❌] Gagal upload final: {e}")

    driver.quit()

# === Loop eksekusi dari upload_log.txt ===
while True:
    log_path = "upload_log.txt"
    if not os.path.exists(log_path):
        time.sleep(5)
        continue

    with open(log_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        print("[⏸] Tidak ada data di upload_log.txt, menunggu...")
        time.sleep(10)
        continue

    current_line = lines[0]
    if ":" not in current_line:
        print(f"[⚠] Format tidak valid: {current_line}")
        with open(log_path, "w", encoding="utf-8") as f:
            f.writelines(lines[1:])
        continue

    username, idpost = current_line.split(":", 1)
    process_upload(username, idpost)

    # Hapus baris yang sudah diproses
    with open(log_path, "w", encoding="utf-8") as f:
        f.writelines([line + "\n" for line in lines[1:]])

    print(f"[🧹] Baris '{current_line}' telah diproses dan dihapus dari upload_log.txt")
    time.sleep(3)