import os
import glob
import subprocess
import psycopg2
from dotenv import load_dotenv

# 1. Pastikan semua variabel ter-load dari .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
BACKUP_DIR = os.getenv("BACKUP_DIR")
PSQL_PATH = r"C:\Program Files\PostgreSQL\18\bin\psql.exe" 

# Database tujuan untuk Analyst
DB_MIRROR = "db_mirror_analyst"

def get_latest_backup():
    """Mencari file .sql dengan waktu modifikasi terbaru"""
    files = glob.glob(os.path.join(BACKUP_DIR, "*.sql"))
    if not files:
        return None
    # Mengambil file yang paling terakhir di-update
    return max(files, key=os.path.getmtime)

def prepare_mirror_db():
    """Menghapus dan membuat ulang DB Mirror (Menghindari Error 25001)"""
    try:
        # Masuk ke lobi 'postgres' menggunakan kredensial dari .env
        conn = psycopg2.connect(
            dbname=DB_NAME, 
            user=DB_USER, 
            password=DB_PASS, 
            host=DB_HOST
        )
        conn.autocommit = True # PENTING: Agar bisa CREATE DATABASE
        cur = conn.cursor()

        # Putus koneksi user lain agar DB bisa di-drop
        cur.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{DB_MIRROR}';")
        
        print(f"🗑️ Membersihkan database {DB_MIRROR} lama...")
        cur.execute(f"DROP DATABASE IF EXISTS {DB_MIRROR};")
        
        print(f"🏗️ Menyiapkan database {DB_MIRROR} baru...")
        cur.execute(f"CREATE DATABASE {DB_MIRROR};")
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Gagal menyiapkan wadah mirror: {e}")
        return False

def run_mirroring():
    print("--- SISTEM UPDATE DATABASE MIRROR ANALYST ---")
    
    # Ambil file backup paling fresh
    latest_file = get_latest_backup()
    
    if not latest_file:
        print("❌ Tidak ditemukan file .sql di folder backup!")
        return

    print(f"📄 File yang digunakan: {os.path.basename(latest_file)}")

    # Jalankan pembersihan DB
    if prepare_mirror_db():
        os.environ['PGPASSWORD'] = DB_PASS
        
        # Perintah Restore
        command = [
            PSQL_PATH,
            "-h", DB_HOST,
            "-U", DB_USER,
            "-d", DB_MIRROR,
            "-f", latest_file
        ]

        try:
            print(f"🔄 Sedang menyalin data ke {DB_MIRROR}. Mohon tunggu...")
            subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"✅ BERHASIL! Database mirror '{DB_MIRROR}' siap digunakan analyst.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Gagal saat proses salin data: {e.stderr}")
        finally:
            if 'PGPASSWORD' in os.environ:
                del os.environ['PGPASSWORD']

if __name__ == "__main__":
    run_mirroring()