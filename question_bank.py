# question_bank.py
"""
question_bank.py
Kumpulan pertanyaan dan jawaban informatika dasar dari file JSON.
"""

import random # Impor modul random untuk mengambil elemen secara acak dari list
import json # Impor modul json untuk memuat data dari file JSON
import os # Impor modul os untuk menangani path file secara portabel antar sistem operasi

def load_questions():
    """
    Fungsi untuk memuat daftar pertanyaan dari file JSON.
    :return: list yang berisi dictionary setiap soal
    """
    # Mendapatkan path lengkap ke file soal.json yang berada dalam folder assets,
    # relatif terhadap lokasi file question_bank.py ini
    json_path = os.path.join(os.path.dirname(__file__), 'assets', 'soal.json')

    # Membuka file JSON dalam mode baca dengan encoding UTF-8
    with open(json_path, 'r', encoding='utf-8') as f:
        # Mengembalikan hasil pembacaan dan parsing file JSON ke dalam bentuk list of dict
        return json.load(f)

def get_random_question():
    """
    Fungsi untuk mengambil satu soal secara acak dari bank soal.
    :return: dictionary yang berisi soal, pilihan jawaban, dan jawaban yang benar
    """
    # Memuat semua soal dari file JSON
    questions = load_questions()

    # Mengambil dan mengembalikan satu soal secara acak dari list soal
    return random.choice(questions)
