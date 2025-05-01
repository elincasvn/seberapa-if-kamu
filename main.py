
import cv2
import time
from quiz_logic import get_soal
from head_tracker import HeadTracker

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Gagal membuka webcam")
        return

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter('output_quiz.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (frame_width, frame_height))

    soal_list = get_soal()
    total_soal = len(soal_list)
    current_soal = 0
    skor = 0

    font = cv2.FONT_HERSHEY_SIMPLEX
    tracker = HeadTracker()
    jawaban_user = None
    start_time = time.time()

    while cap.isOpened() and current_soal < total_soal:
        ret, frame = cap.read()
        if not ret:
            break

        soal = soal_list[current_soal]
        cv2.putText(frame, f"Soal {current_soal + 1}: {soal['pertanyaan']}", (30, 50), font, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Kiri: {soal['opsi'][0]}", (30, 90), font, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"Kanan: {soal['opsi'][1]}", (30, 130), font, 0.6, (0, 255, 0), 2)

        # Deteksi arah kepala
        direction = tracker.detect_direction(frame)
        cv2.putText(frame, f"Arah kepala: {direction}", (30, 170), font, 0.6, (0, 255, 255), 2)

        # Deteksi selama 4 detik, lalu ambil keputusan
        if time.time() - start_time > 4:
            if direction == "left":
                jawaban_user = soal['opsi'][0]
            elif direction == "right":
                jawaban_user = soal['opsi'][1]

            if jawaban_user:
                if jawaban_user == soal['jawaban']:
                    skor += 1
                current_soal += 1
                start_time = time.time()

        out.write(frame)
        cv2.imshow('Seberapa IF Kamu', frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

    # Akhir kuis
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.putText(frame, f"Kuis selesai! Skor kamu: {skor}/{total_soal}", (30, 100), font, 0.9, (0, 255, 255), 2)
        out.write(frame)
        cv2.imshow('Seberapa IF Kamu', frame)
        if cv2.waitKey(3000) & 0xFF == 27:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
