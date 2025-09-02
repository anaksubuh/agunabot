import json
import re

def ambil_data_dan_print(tweet_id, file_path="database.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            database = json.load(f)

        if tweet_id not in database:
            print(f"[ERROR] ID {tweet_id} tidak ditemukan dalam database.")
            return

        data = database[tweet_id]

        # === Header ===
        deskripsi_header = data["header"]["deskripsi"]
        image_header = data["header"]["image"]

        print("Deskripsi Header:")
        print(deskripsi_header)
        print("Gambar Header:")
        for url in image_header:
            print(url)


        # === Threads ===
        threads = data.get("threads", [])
        for i in range(len(threads)):
            deskripsi_thread = threads[i]["deskripsi"]
            image_thread = threads[i]["image"]

            # Cari URL dalam deskripsi thread
            urls_ditemukan = re.findall(r'https?://\S+', deskripsi_thread)

            print("")
            print("="*25)
            print("")
            print(f"Deskripsi Thread {i+1}:")
            print(deskripsi_thread)

            if urls_ditemukan:
                x = "url affiliasi nantinya"
                print("URL dalam deskripsi:")
                for u in urls_ditemukan:
                    print(f'{u} | DI GANTI DENGAN {x}')
                    deskripsi_thread = deskripsi_thread.replace(u, x)

            print(f"Deskripsi Final Thread {i+1}:")
            print(deskripsi_thread)

            print("Gambar Thread:")
            for url in image_thread:
                print(url)

    except Exception as e:
        print(f"[ERROR] Gagal membaca atau memproses file: {e}")

ambil_data_dan_print("1962128420911104181")