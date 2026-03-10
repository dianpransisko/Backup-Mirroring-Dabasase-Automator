@echo off
title Sistem Backup Database Kantor - Manual Mode
color 0E

echo ============================================
echo      MEMULAI BACKUP DATABASE MANUAL
echo ============================================
echo.

:: 1. Masuk ke folder kerja
cd /d ".................."

:: 2. Jalankan Python dan simpan status error-nya
"lokasiinstal python \python.exe" backup_db.py

:: 3. Cek apakah perintah di atas sukses (ErrorLevel 0 = Sukses)
if %ERRORLEVEL% EQU 0 (
    color 0A
    echo.
    echo ============================================
    echo      ✅ BACKUP BERHASIL!
    echo ============================================
    echo Tekan ENTER untuk membuka folder backup...
    pause > nul
    :: 4. Buka folder backup
    start "" "..................\backups"
) else (
    color 0C
    echo.
    echo ============================================
    echo      ❌ BACKUP GAGAL!
    echo ============================================
    echo Periksa pesan error di atas. Pastikan nama file 
    echo 'backup_db.py' sudah benar di folder tersebut.
    echo.
    pause
)

exit