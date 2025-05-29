# main.py
"""
Entry point (titik awal) untuk menjalankan aplikasi filter interaktif seperti di TikTok/Instagram.
Filter ini dirancang untuk menanyakan pertanyaan-pertanyaan seputar informatika.
"""

# Import fungsi utama run_filter dari modul filter.py
from filter import run_filter

# Pemeriksaan apakah file ini dijalankan langsung (bukan diimpor sebagai modul)
if __name__ == "__main__":
    # Jalankan fungsi utama untuk memulai filter interaktif
    run_filter()
