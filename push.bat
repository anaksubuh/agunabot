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

REM === Ambil tanggal dan waktu sekarang ===
for /f "tokens=1-4 delims=/ " %%a in ("%date%") do (
    set day=%%a
    set month=%%b
    set year=%%c
)
for /f "tokens=1-2 delims=: " %%a in ("%time%") do (
    set hour=%%a
    set minute=%%b
)

REM === Format commit message ===
set commitmsg=LAST UPDATE %year%-%month%-%day% %hour%:%minute%

REM === Commit perubahan ===
git commit -m "%commitmsg%"

REM === Set branch utama ===
git branch -M main

REM === Tambahkan remote origin ===
git remote remove origin 2>nul
git remote add origin https://github.com/anaksubuh/agunabot.git

REM === Push ke GitHub ===
git push -u origin main

pause
