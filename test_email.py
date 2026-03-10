import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

def test_kirim():
    print("--- DEBUG PENGIRIMAN EMAIL ---")
    print(f"Mengirim dari: {os.getenv('EMAIL_SENDER')}")
    print(f"Mengirim ke  : {os.getenv('EMAIL_RECEIVER')}")
    
    msg = MIMEMultipart()
    msg['From'] = os.getenv('EMAIL_SENDER')
    msg['To'] = os.getenv('EMAIL_RECEIVER')
    msg['Subject'] = "TEST KONEKSI BACKUP"
    msg.attach(MIMEText("Ini adalah pesan tes. Jika Anda menerima ini, konfigurasi email Anda benar.", 'plain'))

    try:
        print("1. Menghubungkan ke SMTP...")
        server = smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT')))
        server.set_debuglevel(1) # Menampilkan detail komunikasi dengan server
        server.starttls()
        
        print("2. Mencoba Login...")
        server.login(os.getenv('EMAIL_SENDER'), os.getenv('EMAIL_PASSWORD'))
        
        print("3. Mengirim Pesan...")
        server.send_message(msg)
        server.quit()
        print("\n✅ BERHASIL! Email terkirim.")
    except Exception as e:
        print(f"\n❌ GAGAL! Error detail: {e}")

if __name__ == "__main__":
    test_kirim()