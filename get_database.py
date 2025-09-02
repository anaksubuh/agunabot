import json

def get_database_entry(target_id):
    # === Load database.json ===
    with open("database.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if target_id not in data:
        print(f"[❌] ID {target_id} tidak ditemukan di database.json")
        return

    entry = data[target_id]

    # === Header ===
    header_desc = entry["header"]["deskripsi"].replace("\n", "~")
    header_images = entry["header"]["image"]
    print(f"{len(header_images)}|{header_desc}")

    # === Threads ===
    for thread in entry["threads"]:
        thread_desc = thread["deskripsi"].replace("\n", "~")
        thread_images = thread["image"]
        print(f"{len(thread_images)}|{thread_desc}")

    # === Tulis ke file ===
    with open("deskripsi.txt", "w", encoding="utf-8") as out:
        out.write(f"{len(header_images)}|{header_desc}\n")
        for thread in entry["threads"]:
            thread_desc = thread["deskripsi"].replace("\n", "~")
            thread_images = thread["image"]
            out.write(f"{len(thread_images)}|{thread_desc}\n")

# Contoh pemanggilan
get_database_entry("1962128420911104181")
