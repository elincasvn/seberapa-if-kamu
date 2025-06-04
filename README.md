# Seberapa IF sih Kamu?

## Deskripsi
Program ini meniru filter TikTok/Instagram yang menampilkan pertanyaan informatika secara acak di atas video. Pengguna menjawab dengan memiringkan kepala ke kiri atau kanan untuk memilih jawaban, dan skor diberikan di akhir sesi.

## Fitur
- **Kuis Interaktif**: Menampilkan pertanyaan dan dua opsi jawaban.
- **Deteksi Gerakan Kepala**: Menggunakan MediaPipe untuk mengenali gerakan kepala (kiri/kanan) sebagai input jawaban.
- **Bank Soal JSON**: Mengambil pertanyaan secara acak dari file JSON.
- **Overlay Grafis**: Menampilkan pertanyaan dan opsi jawaban di atas feed kamera.
- **Efek Suara**: Memberikan feedback audio (benar/salah) setelah setiap jawaban.
- **Tampilan Skor Akhir**: Menampilkan skor akhir dengan background kustom.
- **Transisi Visual Halus**: Animasi transisi antar pertanyaan dan hasil.
- **Deteksi Pose Stabil**: Menghindari jawaban tidak disengaja dengan memerlukan pose stabil selama beberapa frame.
- **Penempatan Dinamis**: Overlay pertanyaan dan jawaban disesuaikan berdasarkan posisi kepala.

## Persyaratan
- Python **3.8+** (direkomendasikan 3.12.10)
- Webcam
- Speaker/headphone
- Koneksi internet (untuk unduhan awal model MediaPipe)
- Windows dan macOS Support
   - Di Windows, pastikan Python terpasang pada PATH.
   - Di macOS, terutama M1/ARM, pastikan Xcode Command Line Tools telah diinstal:
   ```
   xcode-select --install
   ```
- Catatan khusus untuk instalasi playsound
   - Windows: Gunakan playsound==1.3.0 (biasa berjalan lancar).

   - MacOS: Gunakan pygame sebagai pengganti playsound (lebih stabil untuk efek suara).

## Instalasi untuk pengguna windows

1. Clone Repository
   ```
   git clone https://github.com/elincasvn/seberapa-if-kamu.git
   cd seberapa-if-kamu
   ```
   
3. Buat dan aktifkan virtual environment:
   ```
   python -m venv env
   env\Scripts\activate
   ```
4. Perbarui pip dan install dependencies:
   ```
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Catatan 
   playsound==1.3.0 akan berjalan normal di Windows, jadi tidak perlu perubahan apa pun.

   Tidak perlu install tambahan untuk audio, kecuali jika terjadi masalah saat runtime.

## Menjalankan Program Windows
1. Pastikan virtual environment aktif:
   ```
   # Windows
   env\Scripts\activate
   ```
   
2. Jalankan program:
   ```
   python main.py
   ```
## Instalasi untuk pengguna MacOs

1. Clone Repository
   ```
   git clone https://github.com/elincasvn/seberapa-if-kamu.git
   cd seberapa-if-kamu
   ```

2. Buat dan aktifkan virtual environment:
   ```
   python3 -m venv env
   source env/bin/activate
   ```

3. Hapus playsound dan ganti dengan pygame:
   Karena playsound==1.3.0 sering error di macOS:
   ```
   pip uninstall playsound
   pip install pygame
   ```

4. Install OpenCV (jika perlu):
   Jika terjadi error terkait kamera atau display:
   ```
   pip install opencv-python opencv-python-headless
   ```

5. Perbarui pip dan install dependencies:
   ```
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Catatan Penting:

   Jika playsound tetap dibutuhkan, gunakan versi 1.2.2:

## Menjalankan Program Windows

1. Aktifkan virtual environment:
   ```
   env\Scripts\activate
   ```

2. Jalankan program:
   ```
   python main.py
   ```

# Menjalankan Program MacOs

1. Aktifkan virtual environment:
   ```
   source env/bin/activate
   ```

2. Jalankan program:
   ```
   python main.py
   ```

## Cara Bermain
1. Setelah program berjalan, Anda akan melihat feed webcam.
2. Pertanyaan akan muncul di atas kepala Anda.
3. Miringkan kepala ke:
   - KIRI: untuk memilih jawaban kiri
   - KANAN: untuk memilih jawaban kanan
4. Anda memiliki 20 detik (default question_duration) untuk menjawab setiap pertanyaan.
5. Setelah 5 pertanyaan (default total_questions), skor akhir akan ditampilkan.
6. Tekan q kapan saja untuk skip satu pertanyaan.

## Struktur Folder
```
├── main.py           # Entry point program
├── filter.py         # Logika utama filter & alur permainan
├── question_bank.py  # Pengelola bank soal JSON
├── audio_utils.py    # Utility efek suara
├── video_utils.py    # Utility video & HeadTracker
├── requirements.txt  # Daftar pustaka Python
└── assets/           # Folder aset (gambar, suara, dan bank soal)
    ├── background.png
    ├── pertanyaan.png
    ├── jawaban.png
    ├── soal.json
    ├── sound_ping.mp3
    └── sound_beep.mp3
```

## Assets
- `background.png` : Background untuk tampilan skor
- `pertanyaan.png` : Bubble untuk pertanyaan
- `jawaban.png` : Bubble untuk pilihan jawaban
- `soal.json` : Bank soal dalam format JSON
- `sound_ping.mp3` : Efek suara jawaban benar
- `sound_beep.mp3` : Efek suara jawaban salah

## Format Soal

File soal disimpan di `assets/soal.json`, contoh format:

```json
[
  {
    "question": "Kepanjangan CPU?",
    "option_a": "Central Processing Unit",
    "option_b": "Central Process Unit",
    "answer": "A"
  }
]
```

## Progress

* **2025-04-23**: Pembentukan tim, diskusi ide dan konsep.
* **2025-04-24**: Penentuan konsep, referensi, dan judul proyek.
* **2025-04-27**: Revisi konsep, setup GitHub, implementasi simulasi awal.
* **2025-05-01**: Pengembangan prototype aplikasi.
* **2025-05-02**: Pembaruan `README.md` dan dokumentasi progres.
* **2025-05-29**: Pengerjaan Laporan dan Finalisasi Program.
* **2025-06-04**: Issue Handling (error installing playsound 1.2.2 on macOS)

## Link Demo Program
📁 [Google Drive – Demo Program](https://drive.google.com/drive/folders/1SqHaEJ1cybg_ll-DF9oI0a13RtRJ4o8p?usp=sharing)

## Anggota Tim
* Hasna Dhiya Azizah (121140029) - github.com/121140029
* Dhian Adi Nugraha (121140055) - github.com/dhianadi55
* Elinca Savina (121140073) - github.com/elincasvn
---
