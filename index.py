import base64
import json
import os
import time
import re
import telebot
import datetime
import openpyxl
import pandas as pd
from PIL import Image
import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from streamlit_cookies_manager import EncryptedCookieManager

import openpyxl
wb = openpyxl.Workbook()
ws = wb.active

st.set_page_config(
    page_title='AGUNABOT',
    page_icon='small.gif',
    layout='wide',  
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': 'https://www.extremelycoolapp.com/bug',
         'About': '# This is a header. This is an *extremely* cool app!'
    }
)

with st.sidebar:
    st.image('small.gif',width=50)
    selected = option_menu('Menu', ['Dasboard','Upload','Akun','Scrapper','Database','Setting'], icons=['house','list','book','list','chat','gear'], menu_icon="cast", default_index=0)

if selected == 'Dasboard':
    pass

elif selected == 'Upload':
    import json
    import pandas as pd
    import os

    st.subheader("📤 Upload ID Berdasarkan Akun")

    # === Load username dari profil_output.txt ===
    akun_path = "profil_output.txt"
    akun_data = []
    if os.path.exists(akun_path):
        with open(akun_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) >= 2:
                    akun_data.append(parts[1])  # Ambil username
    else:
        st.warning("File profil_output.txt tidak ditemukan.")

    # === Pilih username ===
    if akun_data:
        selected_username = st.selectbox("Pilih Username Akun", akun_data)
    else:
        selected_username = None

    # === Load ID dari database.json ===
    id_path = "database.json"
    id_list = []
    if os.path.exists(id_path):
        with open(id_path, "r", encoding="utf-8") as f:
            try:
                id_list = json.load(f)
            except Exception as e:
                st.error(f"Gagal membaca database.json: {e}")
    else:
        st.warning("File database.json tidak ditemukan.")

    # === Pilih ID yang mau di-upload ===
    if selected_username and id_list:
        selected_ids = st.multiselect("Pilih ID yang akan di-upload", id_list)

        if st.button("🚀 Antrikan"):
            if selected_ids:
                selected_username = selected_username.lstrip('@')
                st.success(f"{len(selected_ids)} ID akan di-upload untuk akun @{selected_username}")

                # Buat container untuk hasil upload
                with st.container():
                    st.markdown("### ✅ ID yang berhasil diantrikan:")
                    uploaded_list = []

                    with open("upload_log.txt", "a", encoding="utf-8") as log:
                        for id in selected_ids:
                            formatted = f"{selected_username}:{id}"
                            uploaded_list.append(f"- `{formatted}`")
                            log.write(formatted + "\n")

                    # Tampilkan sebagai bullet list
                    st.markdown("\n".join(uploaded_list))

            else:
                st.warning("⚠️ Tidak ada ID yang dipilih untuk di-upload.")
        elif selected_username:
            st.info("ℹ️ Belum ada ID yang tersedia untuk di-upload.")

elif selected == 'Akun':
    import pandas as pd
    from datetime import datetime
    import os

    file_path = "profil_output.txt"

    # Load dan normalisasi data
    data = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) < 7:
                    parts += [""] * (7 - len(parts))  # Tambah kolom kosong
                elif len(parts) > 7:
                    parts = parts[:7]  # Potong jika kelebihan
                data.append(parts)

    # Buat DataFrame tanpa kolom img_url
    df = pd.DataFrame(data, columns=[
        "name", "username", "password", "following", "followers", "status", "last_update"
    ])

    # Hitung metrik
    jumlah_akun = len(df)
    akun_valid = len(df[df["status"].str.upper() == "VALID"])
    akun_invalid = len(df[df["status"].str.upper() == "INVALID"])
    terakhir_update = df["last_update"].max() if not df.empty else "-"

    # Tampilkan metrik
    a, b, c, d = st.columns(4)
    a.metric("Jumlah Akun", f"{jumlah_akun}", "👥", border=True)
    b.metric("VALID", f"{akun_valid}", "✅", border=True)
    c.metric("INVALID", f"{akun_invalid}", "⚠️", border=True)
    d.metric("Terakhir Update", terakhir_update, "🕒", border=True)

    with st.expander("📋 Data Akun"):
        st.subheader("📊 Tabel Akun")
        if not df.empty:
            st.dataframe(df.drop(columns=["last_update"]))
        else:
            st.info("Belum ada data akun yang tersedia.")

    with st.expander("➕ Tambah / Edit Akun"):
        with st.form("akun_form"):
            input_username = st.text_input("Username")
            input_password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Submit")

        if submit:
            output_line = f"~|{input_username}|{input_password}|~|~|proses"
            file_path = "profil_output.txt"

            # Cek apakah baris sudah ada
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    existing_lines = [line.strip() for line in f.readlines()]
            else:
                existing_lines = []
            import autologin
            autologin.autologin(input_username, input_password)

    with st.expander("🗑️ Hapus Akun"):
        if not df.empty:
            akun_hapus = st.selectbox("Pilih username untuk dihapus", df["username"].tolist())
            if st.button("Hapus"):
                df = df[df["username"] != akun_hapus]
                with open(file_path, "w", encoding="utf-8") as f:
                    for _, row in df.iterrows():
                        f.write("|".join(row.astype(str)) + "\n")
                st.warning(f"Akun @{akun_hapus} telah dihapus.")
        else:
            st.info("Tidak ada akun untuk dihapus.")

elif selected == 'Scrapper':
    with st.expander("Scraping twitter thread"):
        st.subheader("🐦 Twitter Thread Scraper")

        twitter_url = st.text_input("Masukkan URL Twitter Thread:")

        if st.button("Simpan URL Twitter"):
            import scraptread
            scraptread.scraptread(st,twitter_url)

    with st.expander("Scraping shopee thread"):
        import converter_url

        st.subheader("🔗 Shopee URL Scraper")

        user_input = st.text_input("Masukkan URL Shopee:")

        if st.button("Submit"):
            st.success(f"URL yang kamu masukkan: {user_input}")
            # Jalankan fungsi pemrosesan
            converter_url.url_produk_split(user_input)

elif selected == 'Database':
    st.title("📊 Statistik Scraping Shopee Threads")

    # Load data dari file JSON
    with open("database.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    jumlah_scrap = len(data)
    jumlah_produk = sum(len(post["threads"]) for post in data.values())

    # Deteksi URL pendek Shopee (dua pola)
    invalid_data = {}
    for post_id, post in data.items():
        urls_pendek = []
        for thread in post["threads"]:
            deskripsi = thread.get("deskripsi", "")
            found_urls = re.findall(r"https://(?:s\.shopee\.co\.id|shope\.ee)/\S+", deskripsi)
            urls_pendek.extend(found_urls)
        if urls_pendek:
            invalid_data[post_id] = urls_pendek

    jumlah_scrap_invalid = len(invalid_data)
    jumlah_scrap_valid = jumlah_scrap - jumlah_scrap_invalid

    # Tampilkan metrik
    a, b, c, d = st.columns(4)
    a.metric("Jumlah Scrap", f"{jumlah_scrap}", "✅", border=True)
    b.metric("Jumlah Produk", f"{jumlah_produk}", "📦", border=True)
    c.metric("INVALID", f"{jumlah_scrap_invalid}", "⚠️", border=True)
    d.metric("VALID", f"{jumlah_scrap_valid}", "👍", border=True)

    # Tampilkan data yang belum dieksekusi
    st.subheader("🔍 Data Belum Di-replace (URL Pendek Shopee)")
    for post_id, urls in invalid_data.items():
        with st.expander(f"ID Post: {post_id}"):
            st.write("🔗 URL Pendek:")
            for url in urls:
                st.write(url)

            replacement_input = st.text_area(
                f"Masukkan URL Final (paste semua, sistem akan auto-split by 'https')", key=post_id
            )

            if st.button(f"Replace URL untuk {post_id}", key=f"replace_{post_id}"):
                # Auto-split berdasarkan 'https'
                raw_split = replacement_input.split("https")
                final_urls = [f"https{part.strip()}" for part in raw_split if part.strip()]

                if len(final_urls) != len(urls):
                    st.error(f"❌ Jumlah URL final ({len(final_urls)}) tidak sama dengan jumlah URL pendek ({len(urls)}).")
                else:
                    # Replace di data
                    idx = 0
                    for thread in data[post_id]["threads"]:
                        original_deskripsi = thread.get("deskripsi", "")
                        found_urls = re.findall(r"https://(?:s\.shopee\.co\.id|shope\.ee)/\S+", original_deskripsi)
                        for short_url in found_urls:
                            original_deskripsi = original_deskripsi.replace(short_url, final_urls[idx])
                            idx += 1
                        thread["deskripsi"] = original_deskripsi

                    # Simpan perubahan ke file
                    with open("database.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    st.success("✅ URL berhasil direplace dan disimpan.")

elif selected == 'Setting':
    pass