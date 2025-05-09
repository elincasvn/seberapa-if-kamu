import cv2
import subprocess
import json
import random
from quiz_logic import Quiz
from head_tracker import HeadTracker
import time
import platform
import subprocess
import os
import shlex
import numpy as np

def play_sound(path):
    system = platform.system()
    if system == "Darwin":  # macOS
        subprocess.Popen(["afplay", path])
    elif system == "Windows":
        # Gunakan 'start' dari cmd, harus melalui shell=True
        subprocess.run(f'start "" "{path}"', shell=True)
    else:
        subprocess.Popen(["aplay", path])  # Linux

def draw_button(frame, text, center, size=(300, 60), color=(0, 140, 255)):
    x, y = center
    w, h = size
    top_left = (x - w // 2, y - h // 2)
    bottom_right = (x + w // 2, y + h // 2)
    cv2.rectangle(frame, top_left, bottom_right, color, -1, cv2.LINE_AA)

    max_width = 260
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 0.6, 1)[0]
    while text_size[0] > max_width:
        text = text[:-1]
        text_size = cv2.getTextSize(text + "...", cv2.FONT_HERSHEY_DUPLEX, 0.6, 1)[0]
        if len(text) <= 4:
            break
    if text_size[0] > max_width:
        text = text[:10] + "..."
    cv2.putText(frame, text + ("..." if text_size[0] > max_width else ""), (x - w // 2 + 10, y + 5),
                cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 1)

def highlight_frame(frame, color=(0, 255, 0), thickness=10):
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (0, 0), (w, h), color, thickness)
    return frame

def ensure_landscape(frame):
    h, w = frame.shape[:2]
    if h > w:
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    return frame

def draw_informatics_frame(frame):
    color = (0, 255, 0)
    thickness = 2
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (10, 10), (w - 10, h - 10), color, thickness)

    corner_size = 25
    for x in [10, w - 10 - corner_size]:
        for y in [10, h - 10 - corner_size]:
            cv2.rectangle(frame, (x, y), (x + corner_size, y + corner_size), color, 1)

def main():
    with open("assets/soal.json", "r") as f:
        questions = json.load(f)

    quiz = Quiz(questions)
    tracker = HeadTracker()

    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    last_answer_time = 0  # Variabel untuk mencatat waktu terakhir jawaban

    while quiz.has_next_question() and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = ensure_landscape(frame)
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (854, 480))  # Landscape format

        # Cek apakah jeda 3 detik sudah selesai
        time_since_last_answer = time.time() - last_answer_time
        if time_since_last_answer < 3:
            # Tampilkan countdown pada layar
            cooldown_time = 3 - int(time_since_last_answer)
            cv2.putText(frame, f"Cooldown: {cooldown_time}s", (300, 240), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
            cv2.imshow("Seberapa IF Kamu?", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue
        else:
            arah = tracker.detect_direction(frame)

        question = quiz.current_question()

        overlay = frame.copy()
        cv2.rectangle(overlay, (20, 20), (834, 80), (10, 50, 90), -1, cv2.LINE_AA)
        alpha = 0.7
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        # Pertanyaan
        cv2.putText(frame, question['question'], (40, 60), font, 0.8, (0, 255, 0), 2)

        # Tombol pilihan di atas kepala
        draw_button(frame, f"A: {question['option_a']}", center=(240, 160), color=(0, 200, 255))
        draw_button(frame, f"B: {question['option_b']}", center=(620, 160), color=(0, 255, 100))

        draw_informatics_frame(frame)

        # Petunjuk jawaban
        cv2.putText(frame, "← Jawab A", (40, 460), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 0), 2)
        cv2.putText(frame, "Jawab B →", (640, 460), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 0), 2)

        if arah:
            answer = "A" if arah == "left" else "B"
            quiz.answer_current_question(answer)
            highlight_color = (0, 255, 0) if answer == question["answer"] else (0, 0, 255)
            frame = highlight_frame(frame, highlight_color, 20)
            sound = "assets/sound_ping.mp3" if answer == question["answer"] else "assets/sound_beep.mp3"
            play_sound(sound)
            quiz.next_question()
            time.sleep(3)  # Ubah jeda menjadi 3 detik
            continue

        cv2.imshow("Seberapa IF Kamu?", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Tampilkan skor akhir pada layar
    result_frame = np.zeros((480, 854, 3), dtype=np.uint8)  # Buat frame kosong
    cv2.putText(result_frame, "Skor Akhir Anda:", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
    cv2.putText(result_frame, f"{quiz.score} / {len(questions)}", (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    # Tampilkan hasil akhir selama 5 detik
    start_time = time.time()
    while time.time() - start_time < 5:
        cv2.imshow("Hasil Akhir", result_frame)
        if cv2.getWindowProperty("Hasil Akhir", cv2.WND_PROP_VISIBLE) < 1:
            break  # Jika jendela ditutup, keluar dari loop

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Tekan 'q' untuk keluar lebih awal
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
