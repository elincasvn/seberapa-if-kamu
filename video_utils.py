# video_utils.py

"""
Utility untuk proses video: head tracking dan overlay pertanyaan/jawaban.
"""

# Impor pustaka eksternal yang diperlukan
import cv2  # OpenCV: untuk manipulasi video dan gambar
import numpy as np  # NumPy: untuk operasi array dan perhitungan numerik
import time  # Digunakan jika perlu menghitung waktu atau delay (tidak digunakan di sini)
import os  # Untuk operasi file path
from collections import deque  # deque: struktur data antrian dua arah untuk riwayat posisi kepala
import mediapipe as mp  # MediaPipe: library Google untuk pelacakan wajah, tangan, dll
from PIL import Image  # PIL: untuk manipulasi gambar (tidak dipakai dalam kode ini)

"""
Kelas HeadTracker
"""

class HeadTracker:
    def __init__(self):
        # Inisialisasi modul face mesh dari MediaPipe
        self.mp_face_mesh = mp.solutions.face_mesh
        # Konfigurasi face mesh: hanya 1 wajah, dengan ambang deteksi & tracking 0.5
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        # Riwayat sudut kepala disimpan dalam deque (terbatas 5 elemen terakhir)
        self.head_pose_history = deque(maxlen=5)

    def get_head_pose(self, frame):
        # Konversi frame dari BGR (OpenCV) ke RGB (MediaPipe)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Proses wajah dengan MediaPipe
        results = self.face_mesh.process(frame_rgb)

        # Jika tidak ada wajah terdeteksi, kembalikan None
        if not results.multi_face_landmarks:
            return None
        
        # Ambil landmark wajah pertama
        face_landmarks = results.multi_face_landmarks[0]
        
        # Ambil posisi atas kepala (landmark ke-10)
        top_head = face_landmarks.landmark[10]
        h, w, _ = frame.shape
        self.head_pos = (int(top_head.x * w), int(top_head.y * h))

        # Hitung sudut kemiringan kepala berdasarkan posisi mata kiri & kanan
        left_eye = face_landmarks.landmark[33]
        right_eye = face_landmarks.landmark[263]
        dx = right_eye.x - left_eye.x
        dy = right_eye.y - left_eye.y
        angle = np.degrees(np.arctan2(dy, dx))  # Ubah dari radian ke derajat
        
        # Simpan sudut dalam riwayat
        self.head_pose_history.append(angle)
        avg_angle = sum(self.head_pose_history) / len(self.head_pose_history)  # Rata-rata sudut

        # Klasifikasikan arah berdasarkan sudut rata-rata
        if avg_angle < -15:
            return "right"  # Menoleh ke kanan
        elif avg_angle > 15:
            return "left"  # Menoleh ke kiri
        return None  # Lurus


"""
Fungsi Utilitas Gambar
"""

def create_bubble_image(width, height, color=(255, 255, 255, 200)):
    """Membuat gambar bubble semi-transparan ukuran tertentu."""
    img = np.zeros((height, width, 4), dtype=np.uint8)  # Buat canvas kosong dengan alpha channel
    # Gambar persegi panjang (bubble) dengan transparansi
    cv2.rectangle(img, (10, 10), (width-10, height-10), color, -1)
    return img

def load_or_create_image(path, default_size=(800, 381)):
    """Memuat gambar dari path, atau membuat gambar default jika gagal."""
    try:
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)  # Baca gambar dengan alpha channel jika ada
        if img is not None:
            if len(img.shape) == 2:
                # Jika grayscale, ubah ke BGRA
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGRA)
            elif len(img.shape) == 3 and img.shape[2] == 3:
                # Jika BGR tanpa alpha, tambahkan alpha
                img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
            return img
    except Exception:
        pass  # Abaikan error jika terjadi

    # Jika gagal load, buat bubble default
    return create_bubble_image(default_size[0], default_size[1])

def load_overlay_images():
    """Memuat gambar overlay untuk pertanyaan, jawaban, dan latar belakang."""
    # Dapatkan direktori 'assets' relatif terhadap file ini
    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))
    
    # Tentukan path file masing-masing gambar
    question_path = os.path.join(assets_dir, "pertanyaan.png")
    answer_path = os.path.join(assets_dir, "jawaban.png")
    background_path = os.path.join(assets_dir, "background.png")
    
    # Muat atau buat gambar dengan ukuran default jika tidak ditemukan
    question_bubble = load_or_create_image(question_path, (400, 120))
    answer_bubble = load_or_create_image(answer_path, (160, 80))
    background = load_or_create_image(background_path, (640, 480))
    
    return question_bubble, answer_bubble, background

def overlay_image(frame, overlay, pos, size=None):
    """Menempatkan gambar RGBA (overlay) ke dalam frame pada posisi tertentu."""
    if size is not None:
        # Resize overlay jika ukuran ditentukan
        overlay = cv2.resize(overlay, size)
    
    if overlay.shape[2] == 4:
        # Ekstrak channel alpha dan normalisasi ke [0, 1]
        alpha = overlay[:, :, 3] / 255.0
        alpha = np.expand_dims(alpha, axis=-1)

        # Gabungkan overlay dengan frame berdasarkan alpha transparency
        for c in range(3):  # Untuk masing-masing channel R, G, B
            frame[pos[1]:pos[1]+overlay.shape[0], 
                  pos[0]:pos[0]+overlay.shape[1], c] = \
                frame[pos[1]:pos[1]+overlay.shape[0], 
                      pos[0]:pos[0]+overlay.shape[1], c] * (1 - alpha[:, :, 0]) + \
                overlay[:, :, c] * alpha[:, :, 0]

    return frame
def overlay_question(frame, question_text, option_a, option_b, head_tracker=None):
    """Overlay question and answer bubbles with text onto the frame."""
    # Muat gambar bubble untuk pertanyaan dan jawaban (dan abaikan background)
    question_bubble, answer_bubble, _ = load_overlay_images()
    # Ambil tinggi (h) dan lebar (w) frame
    h, w = frame.shape[:2]
    
    # Jika head_tracker disediakan dan pernah mendeteksi posisi kepala, ambil head_pos
    head_pos = getattr(head_tracker, 'head_pos', None) if head_tracker else None
    
    # Hitung ukuran bubble pertanyaan: 60% lebar frame, tinggi berdasarkan rasio lebar
    q_width = int(w * 0.6)  
    q_height = int(q_width * 0.3)  
    
    # Tentukan posisi bubble pertanyaan: di atas kepala jika tersedia, atau default
    if head_pos:
        head_x, head_y = head_pos
        # x: center bubble di atas kepala, dibatasi agar tidak keluar frame
        # y: 100px di atas kepala
        q_pos = (
            max(0, min(w - q_width, head_x - q_width // 2)), 
            max(0, head_y - q_height - 100)
        )
    else:
        # jika kepala tidak terdeteksi, letakkan di tengah atas frame
        q_pos = (w // 2 - q_width // 2, int(h * 0.12))
    
    # Ukuran bubble jawaban: 22% lebar frame, 35% tinggi frame
    a_width = int(w * 0.22)
    a_height = int(h * 0.35)
    
    if head_pos:
        head_x, head_y = head_pos
        vertical_offset = 50  # jarak vertikal 50px di atas kepala
        # kiri: 50px ke kiri kepala; kanan: 50px ke kanan kepala
        a_left_pos = (
            max(0, head_x - a_width - 50),
            max(0, head_y - vertical_offset)
        )
        a_right_pos = (
            min(w - a_width, head_x + 50),
            max(0, head_y - vertical_offset)
        )
    else:
        # posisi default kiri dan kanan bawah pertanyaan
        a_left_pos = (int(w * 0.25) - a_width // 2, int(h * 0.45))
        a_right_pos = (int(w * 0.75) - a_width // 2, int(h * 0.45))
    
    # Tempel bubble gambar sebelum menggambar teks (agar alpha channel ikut diterapkan)
    frame = overlay_image(frame, question_bubble, q_pos, (q_width, q_height))
    frame = overlay_image(frame, answer_bubble, a_left_pos, (a_width, a_height))
    frame = overlay_image(frame, answer_bubble, a_right_pos, (a_width, a_height))
    
    # Konfigurasi font untuk teks
    font = cv2.FONT_HERSHEY_SIMPLEX
    q_font_scale = 0.7
    a_font_scale = 0.65
    color = (0, 0, 0)  # hitam
    thickness = 2
    
    # ----- Gambar latar teks bubble (putih) -----
    
    # Pertanyaan: gambar rectangle putih penuh
    cv2.rectangle(
        frame,
        (q_pos[0], q_pos[1]),
        (q_pos[0] + q_width, q_pos[1] + q_height),
        (255, 255, 255),  # putih
        -1  # fill
    )
    
    # Jawaban: white fill + border abu-abu untuk kesan rounded (sekilas)
    for pos in [a_left_pos, a_right_pos]:
        # fill putih
        cv2.rectangle(
            frame,
            (pos[0], pos[1]),
            (pos[0] + a_width, pos[1] + a_height),
            (255, 255, 255),
            -1
        )
        # border tipis untuk efek bayangan
        cv2.rectangle(
            frame,
            (pos[0], pos[1]),
            (pos[0] + a_width, pos[1] + a_height),
            (200, 200, 200),  # abu-abu
            2
        )
    
    # ----- Word wrap dan gantung teks pertanyaan -----
    
    words = question_text.split()
    lines = []
    current_line = []
    max_width = int(q_width * 0.9)  # gunakan 90% dari lebar bubble
    
    for word in words:
        current_line.append(word)
        text = " ".join(current_line)
        size = cv2.getTextSize(text, font, q_font_scale, thickness)[0]
        
        if size[0] > max_width:
            # Jika satu kata saja sudah terlalu panjang, potong di tengah
            if len(current_line) == 1:
                half_len = len(word) // 2
                lines.append(word[:half_len] + "-")
                current_line = [word[half_len:]]
            else:
                # pindahkan kata terakhir ke baris baru
                lines.append(" ".join(current_line[:-1]))
                current_line = [word]
    # simpan sisa kata di baris terakhir
    if current_line:
        text = " ".join(current_line)
        size = cv2.getTextSize(text, font, q_font_scale, thickness)[0]
        if size[0] > max_width and len(current_line) == 1:
            word = current_line[0]
            half_len = len(word) // 2
            lines.append(word[:half_len] + "-")
            lines.append(word[half_len:])
        else:
            lines.append(text)
    
    # Gambar tiap baris teks pertanyaan, dengan spasi vertikal proporsional
    line_spacing = 1.3
    for i, line in enumerate(lines):
        size = cv2.getTextSize(line, font, q_font_scale, thickness)[0]
        text_x = q_pos[0] + (q_width - size[0]) // 2
        text_y = q_pos[1] + (q_height // 4) + int(i * size[1] * line_spacing)
        cv2.putText(frame, line, (text_x, text_y), font, q_font_scale, color, thickness)
    
    # ----- Word wrap dan gambar teks opsi jawaban -----
    
    for text, pos in [(option_a, a_left_pos), (option_b, a_right_pos)]:
        words = text.split()
        lines = []
        current_line = []
        max_width = int(a_width * 0.9)
        
        for word in words:
            current_line.append(word)
            line_text = " ".join(current_line)
            size = cv2.getTextSize(line_text, font, a_font_scale, thickness)[0]
            if size[0] > max_width:
                if len(current_line) == 1:
                    half_len = len(word) // 2
                    lines.append(word[:half_len] + "-")
                    current_line = [word[half_len:]]
                else:
                    lines.append(" ".join(current_line[:-1]))
                    current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
        
        # Gambar tiap baris teks jawaban
        for i, line in enumerate(lines):
            size = cv2.getTextSize(line, font, a_font_scale, thickness)[0]
            text_x = pos[0] + (a_width - size[0]) // 2
            line_height = int(size[1] * 1.5)
            text_y = pos[1] + (a_height // 4) + i * line_height
            cv2.putText(frame, line, (text_x, text_y), font, a_font_scale, color, thickness)
    
    return frame


def overlay_score(frame, score, total):
    """Overlay final score with background image."""
    # Muat hanya background dari aset
    _, _, background = load_overlay_images()
    h, w = frame.shape[:2]
    
    # Resize background untuk menutupi seluruh frame
    background = cv2.resize(background, (w, h))
    
    # Siapkan teks skor
    score_text = f"Score: {score}/{total}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    color = (255, 255, 255)  # putih
    thickness = 3
    
    # Hitung ukuran teks untuk memposisikan di tengah
    size = cv2.getTextSize(score_text, font, font_scale, thickness)[0]
    text_x = (w - size[0]) // 2
    text_y = (h + size[1]) // 2
    
    # Overlay background, kemudian gambar teks skor di atasnya
    frame = overlay_image(frame, background, (0, 0))
    cv2.putText(frame, score_text, (text_x, text_y), font, font_scale, color, thickness)
    
    return frame
