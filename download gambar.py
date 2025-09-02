import json
import requests
import os

def is_valid_image(url):
    """Filter hanya gambar jpg dengan name=360x360, bukan SVG atau profile_images"""
    return (
        url.endswith("jpg&name=360x360") and
        ".svg" not in url and
        "profile_images" not in url
    )

def download_image(url, filename, folder):
    """Download gambar jika valid"""
    filepath = os.path.join(folder, filename)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"✅ Saved: {filename}")
        else:
            print(f"❌ Failed to download {url} (status {response.status_code})")
    except Exception as e:
        print(f"⚠️ Error downloading {url}: {e}")

# Load database
with open("database.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Target ID
target_id = "1962328768665841741"
entry = data.get(target_id)

# Buat folder output
output_folder = "downloaded_images"
os.makedirs(output_folder, exist_ok=True)

# Download header images
header_images = entry["header"]["image"]
for idx, url in enumerate(header_images, start=1):
    if is_valid_image(url):
        filename = f"header{idx}.jpg"
        download_image(url, filename, output_folder)

# Download thread images
threads = entry["threads"]
for thread_idx, thread in enumerate(threads, start=1):
    for image_idx, url in enumerate(thread["image"], start=1):
        if is_valid_image(url):
            filename = f"gambar{thread_idx}.{image_idx}.jpg"
            download_image(url, filename, output_folder)
