import json
import requests
import os

def scrap_gambar(target_id):
    def is_valid_image(url):
        """Filter hanya gambar jpg dan bukan SVG atau profile_images"""
        return (
            "format=jpg" in url and
            ".svg" not in url and
            "profile_images" not in url
        )

    def download_image(url, filename, folder):
        """Download gambar jika valid"""
        filepath = os.path.join(folder, filename)
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print(f"✅ Saved: {filename}")
            else:
                print(f"❌ Failed to download {url} (status {response.status_code})")
        except Exception as e:
            print(f"⚠️ Error downloading {url}: {e}")

    # Load database
    try:
        with open("database.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("[❌] File database.json tidak ditemukan.")
        return
    except json.JSONDecodeError as e:
        print(f"[❌] Format JSON error: {e}")
        return

    entry = data.get(target_id)
    if not entry:
        print(f"[❌] ID {target_id} tidak ditemukan di database.json")
        return

    output_folder = "downloaded_images"
    os.makedirs(output_folder, exist_ok=True)

    # Header images
    header_images = entry.get("header", {}).get("image", [])
    for idx, raw_url in enumerate(header_images, start=1):
        if is_valid_image(raw_url):
            filename = f"header{idx}.jpg"
            download_image(raw_url, filename, output_folder)

    # Thread images
    threads = entry.get("threads", [])
    for thread_idx, thread in enumerate(threads, start=1):
        for image_idx, raw_url in enumerate(thread.get("image", []), start=1):
            if is_valid_image(raw_url):
                filename = f"gambar{thread_idx}.{image_idx}.jpg"
                download_image(raw_url, filename, output_folder)

# Contoh pemanggilan
scrap_gambar("1545393613685010432")  # Ganti dengan ID tweet yang diinginkan
