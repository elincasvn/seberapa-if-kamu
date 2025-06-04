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
   - Jika mengalami kegagalan instalasi playsound==1.3.0 di macOS ARM, ganti ke playsound==1.2.2.
   - Pada Windows, playsound==1.3.0 biasanya terinstal tanpa masalah.
   - Alternatif lain (cross-platform): gunakan simpleaudio, python-vlc, atau pygame.

## Instalasi
1. Clone Repository
   Jalankan Perintah:
   ```
   git clone https://github.com/username/repo.git
   cd repo

   ```

2. Buat dan aktifkan virtual environment:
   ```
   python -m venv env

   # Windows
   env\Scripts\activate

   # macOS/Linux
   source env/bin/activate
   ```

3. Perbarui pip, setuptools, dan wheel
   ```
   pip install --upgrade pip setuptools wheel
   ```

4. Install dependencies:
   ```
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
   - Jika pada Windows: playsound==1.3.0 biasanya terinstal tanpa masalah.
   - Jika pada macOS ARM muncul error:
      1. Buka file requirements.txt, ubah:
         ```
         playsound==1.3.0
         ```
         menjadi
         ```
         playsound==1.2.2
         ```
      2. Jalankan ulang:
         ```
         pip install -r requirements.txt
         ```
      3. Jika tetap ingin playsound==1.3.0, paksa instal tanpa binary:
         ```
         pip install --no-binary :all: playsound==1.3.0
         ```

## Menjalankan Program
1. Pastikan virtual environment aktif:
   ```
   # Windows
   env\Scripts\activate

   # macOS/Linux
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
