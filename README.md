# Seberapa IF Sih Kamu?

Game filter interaktif berbasis Python dan OpenCV untuk menguji pengetahuan dasar Informatika melalui gerakan kepala. Pengguna akan menjawab soal pilihan ganda yang ditampilkan secara acak, dan mendapatkan skor di akhir kuis. Aplikasi ini dibangun untuk tugas proyek mata kuliah IF4021.

## Daftar Isi

* [Deskripsi Proyek](#deskripsi-proyek)
* [Fitur](#fitur)
* [Tools dan Teknologi](#tools-dan-teknologi)
* [Anggota Tim](#anggota-tim)
* [Progres](#progres)
* [Instalasi](#instalasi)
* [Penggunaan](#penggunaan)
* [Struktur Proyek](#struktur-proyek)
* [Lisensi](#lisensi)

## Deskripsi Proyek

“Seberapa IF sih kamu?” adalah game berbasis filter TikTok yang menguji pengetahuan dasar Informatika melalui gerakan kepala dan pilihan ganda. Setiap pengguna akan diberikan serangkaian soal dengan dua opsi jawaban. Jawaban benar akan menambah skor, yang kemudian ditampilkan di akhir kuis.

Proyek ini berawal dari konsep filter TikTok dan dikembangkan menjadi aplikasi kuis interaktif menggunakan Python dan OpenCV, lengkap dengan logika penilaian dan simulasi scoring.

## Fitur

* **Pertanyaan acak**
  Soal ditampilkan secara acak setiap kali permainan dimulai.
* **Dua pilihan jawaban**
  Setiap soal menyediakan dua opsi jawaban.
* **Skor akhir**
  Pengguna memperoleh skor berdasarkan jumlah jawaban benar.
* **Integrasi TikTok Effect House**
  Antarmuka dan gestur menggunakan TikTok Effect House.
* **Simulasi logika di Python**
  Logika permainan dan scoring diimplementasikan menggunakan Python.
* **Deteksi gerakan kepala**
  Interaksi dengan aplikasi melalui deteksi gerakan kepala memakai OpenCV.

## Tools dan Teknologi

* **TikTok Effect House**
  Membuat filter dan antarmuka di TikTok.
* **Python**
  Implementasi logika, scoring, dan penyusunan soal.
* **OpenCV**
  Deteksi wajah dan gerakan kepala, serta pengolahan gambar.
* **GitHub**
  Manajemen kode dan kolaborasi tim.

## Anggota Tim

* Elinca Savina (121140073)
* Hasna Dhiya Azizah (121140029)
* Dhian Adi Nugraha (121140055)

## Progres

* **2025-04-23**: Pembentukan tim, diskusi ide dan konsep.
* **2025-04-24**: Penentuan konsep, referensi, dan judul proyek.
* **2025-04-27**: Revisi konsep, setup GitHub, implementasi simulasi awal.
* **2025-05-01**: Pengembangan prototype aplikasi.
* **2025-05-02**: Pembaruan `README.md` dan dokumentasi progres.

## Instalasi

1. Clone repositori:

   ```bash
   git clone https://github.com/dhianadi55/seberapa-if-kamu.git
   ```
2. Masuk ke direktori proyek:

   ```bash
   cd seberapa-if-kamu
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Penggunaan

Jalankan notebook utama menggunakan perintah berikut:

```bash
jupyter nbconvert --to notebook --execute main.ipynb --inplace
```

Perintah ini akan mengeksekusi `main.ipynb` dan memperbarui notebook yang sama.
Jika Anda ingin menjalankan aplikasi sebagai script, konversi terlebih dahulu notebook ke script Python:

```bash
jupyter nbconvert --to script main.ipynb
python main.py
```

## Struktur Proyek

```bash
tree .
├── main.ipynb         # Notebook utama: logika permainan dan scoring
├── modules/           # Modul utama (deteksi wajah, logika game, render UI)
└── data/
    └── questions.json # File soal kuis
```

## Lisensi

Proyek ini dilisensikan di bawah **MIT License**.
Lihat [LICENSE](./LICENSE) untuk detail.
