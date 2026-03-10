import subprocess
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# 1. Pastikan load_dotenv terpanggil paling atas
load_dotenv()

# --- AMBIL KONFIGURASI (Pastikan nama variabel sama dengan .env) ---
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
PG_DUMP_PATH = os.getenv("PG_DUMP_PATH")
BACKUP_DIR = os.getenv("BACKUP_DIR")

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")

def send_email_notification(subject, body):
    """Fungsi send email"""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT))
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("📧 Notifikasi Email BERHASIL terkirim!")
    except Exception as e:
        print(f"❌ Gagal kirim email: {e}")

def backup_database():
    # Validasi folder
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"{DB_NAME}_{timestamp}.sql"
    filepath = os.path.join(BACKUP_DIR, filename)

    os.environ['PGPASSWORD'] = DB_PASS
    command = [
        PG_DUMP_PATH,
        "-h", DB_HOST,
        "-U", DB_USER,
        "-d", DB_NAME,
        "-f", filepath
    ]

    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Memulai backup...")
        # Jalankan proses backup
        subprocess.run(command, check=True, capture_output=True, text=True)
        
        # JIKA SUKSES -> KIRIM EMAIL
        subject = f"✅ SUCCESS: Backup Database {DB_NAME} pada {datetime.now()}"
        body = f"Laporan Backup:\n\nDatabase: {DB_NAME}\nFile: {filename}\nWaktu: {datetime.now()}\nStatus: DATABASE BACKUP SUCCESSFUL BACKUP."
        send_email_notification(subject, body) # Memanggil fungsi email
        
        print(f"✅ BERHASIL! File: {filename}")
        
    except subprocess.CalledProcessError as e:
        # JIKA GAGAL -> KIRIM EMAIL ERROR
        subject = f"❌ FAILED: Backup Database {DB_NAME}"
        body = f"PERINGATAN!\n\nBackup gagal.\nError: {e.stderr}"
        send_email_notification(subject, body)
        print(f"❌ GAGAL! Error: {e.stderr}")
    finally:
        if 'PGPASSWORD' in os.environ:
            del os.environ['PGPASSWORD']

if __name__ == "__main__":
    backup_database()