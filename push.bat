@echo off
REM === Setup Git Ignore ===
echo profile/ > .gitignore
echo default.txt >> .gitignore
echo downloaded_images >> .gitignore
echo __pycache__ >> .gitignore

REM === Inisialisasi Git ===
git init

REM === Tambahkan semua file kecuali yang di-ignore ===
git add .

REM === Commit perubahan ===
git commit -m "Update semua file kecuali folder profile dan file profilepath.txt"

REM === Set branch utama ===
git branch -M main

REM === Tambahkan remote origin ===
git remote remove origin 2>nul
git remote add origin https://github.com/anaksubuh/agunabot.git

REM === Push ke GitHub ===
git push -u origin main

pause