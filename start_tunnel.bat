@echo off
title LocalTunnel Auto Reconnect
color 0A

:RESTART
echo [INFO] Menjalankan LocalTunnel pada subdomain: mycloud
lt --port 8502 --subdomain mycloud

echo [ERROR] LocalTunnel berhenti atau error. Mencoba menghubungkan kembali!!!
goto RESTART
